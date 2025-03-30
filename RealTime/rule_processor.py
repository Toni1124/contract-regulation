import json
from decimal import Decimal
import time

class RuleProcessor:
    def __init__(self, db_config):
        self.db_config = db_config
        self.contract_rules = {}
        self.last_rules_update = 0
        self.rules_update_interval = 60  # 每60秒更新一次规则

    def load_rules(self, cursor):
        """加载所有规则"""
        current_time = time.time()
        
        # 如果距离上次更新时间不足规定间隔，直接返回缓存的规则
        if current_time - self.last_rules_update < self.rules_update_interval:
            return self.contract_rules

        query = """
        SELECT contract_address, functions 
        FROM "default".rules_new
        """
        cursor.execute(query)
        rules = cursor.fetchall()
        
        # Debug: 打印规则数据
        print("\n加载规则:")
        
        # 清空并重新加载规则
        self.contract_rules = {}
        for contract_address, functions in rules:
            try:
                addr = contract_address.lower()
                if addr not in self.contract_rules:
                    self.contract_rules[addr] = []
                
                # Debug: 打印原始数据
                print(f"合约地址: {addr}")
                print(f"Functions类型: {type(functions)}")
                print(f"Functions内容: {functions}")
                
                # 根据functions的类型进行处理
                if isinstance(functions, str):
                    # 如果是字符串，需要解析
                    functions_data = json.loads(functions)
                elif isinstance(functions, (list, dict)):
                    # 如果已经是列表或字典，直接使用
                    functions_data = functions
                else:
                    print(f"⚠️ 未知的functions类型: {type(functions)}")
                    continue
                
                if isinstance(functions_data, list):
                    self.contract_rules[addr].extend(functions_data)
                else:
                    self.contract_rules[addr].append(functions_data)
                
            except Exception as e:
                print(f"❌ 处理规则时出错 (地址: {contract_address}): {str(e)}")
                continue
        
        self.last_rules_update = current_time
        
        # Debug: 打印处理后的规则
        print("\n处理后的规则:")
        for addr, rules in self.contract_rules.items():
            print(f"地址: {addr}")
            print(f"规则: {rules}")
        
        return self.contract_rules

    def check_parameter_condition(self, param_rule, actual_value):
        """检查参数是否符合条件"""
        try:
            rule_value = Decimal(param_rule['value'])
            actual_value = Decimal(actual_value)
            condition = param_rule['condition']

            if condition == '<=':
                return actual_value <= rule_value, f"值 {actual_value} 应小于等于 {rule_value}"
            elif condition == '<':
                return actual_value < rule_value, f"值 {actual_value} 应小于 {rule_value}"
            elif condition == '>=':
                return actual_value >= rule_value, f"值 {actual_value} 应大于等于 {rule_value}"
            elif condition == '>':
                return actual_value > rule_value, f"值 {actual_value} 应大于 {rule_value}"
            elif condition == '==':
                return actual_value == rule_value, f"值 {actual_value} 应等于 {rule_value}"
            else:
                return False, f"未知的条件类型: {condition}"
        except Exception as e:
            return False, f"参数比较出错: {str(e)}"

    def check_transaction(self, tx_dict, cursor):
        """检查单个交易是否符合规则"""
        try:
            # 每次检查交易时都尝试更新规则
            contract_rules = self.load_rules(cursor)
            
            to_address = tx_dict['to_address'].lower()
            function_name = tx_dict['function_name']
            
            # Debug: 打印交易信息
            print(f"检查交易: {to_address}")
            print(f"函数名: {function_name}")
            
            # 处理 decoded_parameters
            try:
                if isinstance(tx_dict['decoded_parameters'], str):
                    decoded_params = json.loads(tx_dict['decoded_parameters'])
                elif isinstance(tx_dict['decoded_parameters'], (dict, list)):
                    decoded_params = tx_dict['decoded_parameters']
                else:
                    decoded_params = {}
            except Exception as e:
                print(f"解析参数错误: {str(e)}")
                print(f"原始参数: {tx_dict['decoded_parameters']}")
                decoded_params = {}

            # 如果合约没有规则，默认通过
            if to_address not in contract_rules:
                return True, "通过监管"

            # 检查该合约的所有规则
            for rule in contract_rules[to_address]:
                if rule['name'] == function_name:
                    for param_rule in rule['params']:
                        param_name = param_rule['name']
                        if param_name not in decoded_params:
                            return False, f"未通过监管，缺少参数 {param_name}"
                        
                        passed, message = self.check_parameter_condition(
                            param_rule, 
                            decoded_params[param_name]
                        )
                        if not passed:
                            return False, f"未通过监管，函数 {function_name} 的参数 {param_name} {message}"

            return True, "通过监管"
            
        except Exception as e:
            print(f"规则检查错误: {str(e)}")
            return False, f"规则检查出错: {str(e)}"

    def update_transaction_rules_check(self, cursor, tx_dict, check_result, check_message):
        """更新交易的规则检查结果"""
        update_query = """
        UPDATE eth_transaction_details 
        SET rules_check_passed = %s, 
            rules_check_message = %s
        WHERE block_number = %s 
        AND transaction_index = %s
        """
        cursor.execute(update_query, (
            check_result,
            check_message,
            tx_dict['block_number'],
            tx_dict['transaction_index']
        ))

    def recheck_transactions(self, conn, contract_addresses=None):
        """
        重新检查已存在的交易
        :param conn: 数据库连接
        :param contract_addresses: 可选，指定要重新检查的合约地址列表
        """
        try:
            print("\n🔄 开始重新检查交易...")
            cursor = conn.cursor()
            
            # 构建查询条件
            where_clause = ""
            query_params = []
            if contract_addresses:
                addresses = [addr.lower() for addr in contract_addresses]
                where_clause = "WHERE LOWER(to_address) = ANY(%s)"
                query_params = [addresses]

            query = f"""
            SELECT block_number, transaction_index, to_address, 
                   function_name, decoded_parameters
            FROM eth_transaction_details
            {where_clause}
            ORDER BY block_number, transaction_index
            """
            
            cursor.execute(query, query_params)
            transactions = cursor.fetchall()
            
            if not transactions:
                print("ℹ️ 没有找到需要重新检查的交易")
                return

            print(f"📝 找到 {len(transactions)} 笔交易需要重新检查")
            
            # 加载最新规则
            self.last_rules_update = 0
            contract_rules = self.load_rules(cursor)
            
            success_count = 0
            error_count = 0
            
            for tx in transactions:
                try:
                    block_number, tx_index, to_address, func_name, decoded_params = tx
                    
                    # Debug: 打印交易信息
                    print(f"\n检查交易: Block={block_number}, Index={tx_index}")
                    print(f"Function: {func_name}")
                    print(f"Decoded params type: {type(decoded_params)}")
                    print(f"Decoded params: {decoded_params}")
                    
                    # 确保 decoded_params 是字符串格式
                    if decoded_params is not None and not isinstance(decoded_params, str):
                        # 如果已经是字典或列表，直接转换为JSON字符串
                        decoded_params = json.dumps(decoded_params)
                    
                    tx_dict = {
                        'block_number': block_number,
                        'transaction_index': tx_index,
                        'to_address': to_address,
                        'function_name': func_name,
                        'decoded_parameters': decoded_params
                    }
                    
                    # 检查规则
                    check_result, check_message = self.check_transaction(tx_dict, cursor)
                    
                    # 更新检查结果
                    self.update_transaction_rules_check(
                        cursor,
                        tx_dict,
                        check_result,
                        check_message
                    )
                    
                    success_count += 1
                    if success_count % 100 == 0:
                        print(f"✅ 已重新检查 {success_count}/{len(transactions)} 笔交易")
                    
                    conn.commit()
                    
                except Exception as e:
                    error_count += 1
                    print(f"❌ 重新检查交易出错 (block={block_number}, tx_index={tx_index})")
                    print(f"   错误信息: {str(e)}")
                    print(f"   交易数据: {tx}")
                    conn.rollback()
                    continue
            
            print(f"\n📊 重新检查完成:")
            print(f"   - 成功: {success_count}")
            print(f"   - 失败: {error_count}")
            print(f"   - 总计: {len(transactions)}")
            
        except Exception as e:
            print(f"❌ 重新检查过程出错: {str(e)}")
            raise
        finally:
            cursor.close()
