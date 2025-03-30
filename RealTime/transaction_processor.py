import psycopg2
from multiprocessing import Pool, cpu_count
from config import DB_CONFIG, BATCH_SIZE, MAX_WORKERS
from abi_manager import ABIManager
from logger import logger
from tqdm import tqdm
import time
import json
from rule_processor import RuleProcessor

class TransactionProcessor:
    def __init__(self):
        self.max_processes = cpu_count()*2  # 使用CPU核心数量作为进程数
        
    def process_batch_worker(self, batch_params):
        """
        工作进程处理单个批次
        """
        start_block, end_block, contract_addresses = batch_params
        conn = None
        cursor = None
        try:
            print(f"\n📦 进程开始处理批次: {start_block} -> {end_block}")
            conn = psycopg2.connect(**DB_CONFIG)
            cursor = conn.cursor()
            
            # 在每个工作进程中创建新的ABIManager实例
            abi_manager = ABIManager()
            
            # 初始化规则处理器
            rule_processor = RuleProcessor(DB_CONFIG)
            
            # 加载所有规则 - 不使用with语句
            contract_rules = rule_processor.load_rules(cursor)
            
            # 获取原始交易数据
            query = """
            SELECT * FROM "default".eth_transaction
            WHERE block_number BETWEEN %s AND %s
            AND to_address = ANY(%s)
            ORDER BY block_number, transaction_index
            """
            
            cursor.execute(query, (start_block, end_block, contract_addresses))
            transactions = cursor.fetchall()
            
            if not transactions:
                print(f"ℹ️ 区块 {start_block}-{end_block} 没有找到交易")
                return 0, 0

            print(f"🔍 区块 {start_block}-{end_block} 找到 {len(transactions)} 笔交易")
            
            # 获取列名
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_schema = 'default' 
                AND table_name = 'eth_transaction' 
                ORDER BY ordinal_position
            """)
            columns = [col[0] for col in cursor.fetchall()]
            
            success_count = 0
            error_count = 0
            
            # 处理每个交易
            for tx in transactions:
                try:
                    tx_dict = dict(zip(columns, tx))
                    
                    to_address = tx_dict.get('to_address')
                    if not to_address:
                        continue
                    
                    input_data = tx_dict.get('input')
                    if not input_data:
                        input_data = '0x'
                    
                    # 使用局部的abi_manager
                    func_signature, func_name, decoded_params = abi_manager.decode_input(
                        to_address.strip(), input_data
                    )
                    
                    # 准备插入数据
                    insert_data = [
                        tx_dict.get('block_number'),
                        tx_dict.get('block_timestamp'),
                        tx_dict.get('transaction_index'),
                        tx_dict.get('value'),
                        tx_dict.get('gas'),
                        tx_dict.get('gas_price'),
                        tx_dict.get('nonce'),
                        tx_dict.get('from_address'),
                        tx_dict.get('to_address'),
                        tx_dict.get('receipt_contract_address'),
                        tx_dict.get('receipt_root'),
                        tx_dict.get('block_hash'),
                        tx_dict.get('input'),
                        tx_dict.get('blob_versioned_hashes'),
                        tx_dict.get('hash'),
                        func_signature,
                        func_name,
                        json.dumps(decoded_params) if decoded_params else None
                    ]
                    
                    # 使用具体的列名进行插入
                    insert_query = """
                    INSERT INTO eth_transaction_details (
                        block_number, block_timestamp, transaction_index, value, gas, 
                        gas_price, nonce, from_address, to_address, receipt_contract_address,
                        receipt_root, block_hash, input, blob_versioned_hashes, hash,
                        function_signature, function_name, decoded_parameters
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (block_number, transaction_index) DO UPDATE SET
                        function_signature = EXCLUDED.function_signature,
                        function_name = EXCLUDED.function_name,
                        decoded_parameters = EXCLUDED.decoded_parameters;
                    """
                    
                    cursor.execute(insert_query, insert_data)
                    
                    # 规则检查使用同一个cursor
                    if func_name and decoded_params:
                        tx_dict = {
                            'block_number': insert_data[0],
                            'transaction_index': insert_data[2],
                            'to_address': insert_data[8],
                            'function_name': func_name,
                            'decoded_parameters': json.dumps(decoded_params)
                        }
                        
                        check_result, check_message = rule_processor.check_transaction(
                            tx_dict, 
                            cursor  # 使用同一个cursor
                        )
                        
                        rule_processor.update_transaction_rules_check(
                            cursor,  # 使用同一个cursor
                            tx_dict,
                            check_result,
                            check_message
                        )
                    else:
                        tx_dict = {
                            'block_number': insert_data[0],
                            'transaction_index': insert_data[2]
                        }
                        rule_processor.update_transaction_rules_check(
                            cursor,  # 使用同一个cursor
                            tx_dict,
                            True,
                            "通过监管（无需解码的交易）"
                        )
                    
                    conn.commit()
                    success_count += 1
                    
                except Exception as e:
                    conn.rollback()
                    error_count += 1
                    print(f"❌ Error processing transaction at block={tx_dict.get('block_number', 'unknown')}: {str(e)}")
                    continue
            
            return success_count, error_count

        except Exception as e:
            print(f"❌ Batch error {start_block}-{end_block}: {str(e)}")
            return 0, 0
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def process_range(self, begin_block, end_block, contract_addresses):
        """
        使用多进程处理区块范围
        """
        print(f"\n🚀 开始处理区块范围: {begin_block} -> {end_block}")
        
        # 计算批次
        batches = []
        current_block = begin_block
        while current_block < end_block:
            batch_end = min(current_block + BATCH_SIZE, end_block)
            batches.append((current_block, batch_end, contract_addresses))
            current_block = batch_end + 1
        
        total_batches = len(batches)
        print(f"📑 总批次数: {total_batches}")
        print(f"💻 使用进程数: {self.max_processes}")
        
        start_time = time.time()
        
        # 使用进程池处理批次
        with Pool(processes=self.max_processes) as pool:
            results = pool.map(self.process_batch_worker, batches)
        
        # 统计结果
        total_success = sum(success for success, _ in results)
        total_errors = sum(errors for _, errors in results)
        
        total_time = time.time() - start_time
        print(f"\n✨ 处理完成:")
        print(f"   - 总耗时: {total_time:.2f}秒")
        print(f"   - 成功: {total_success}")
        print(f"   - 失败: {total_errors}")
        print(f"   - 平均每批次耗时: {total_time/total_batches:.2f}秒")

    def recheck_existing_transactions(self, contract_addresses=None):
        """
        重新检查已存在的交易
        :param contract_addresses: 可选，指定要重新检查的合约地址列表
        """
        try:
            print("\n🚀 开始重新检查已存在的交易...")
            conn = psycopg2.connect(**DB_CONFIG)
            
            # 初始化规则处理器
            rule_processor = RuleProcessor(DB_CONFIG)
            
            # 执行重新检查
            rule_processor.recheck_transactions(conn, contract_addresses)
            
            print("✨ 重新检查完成")
            
        except Exception as e:
            print(f"❌ 重新检查过程出错: {str(e)}")
        finally:
            if conn:
                conn.close()

    def warm_up_pool(self):
        """预热进程池，避免冷启动开销"""
        with Pool(processes=self.max_processes) as pool:
            pool.map(lambda x: None, range(self.max_processes))
