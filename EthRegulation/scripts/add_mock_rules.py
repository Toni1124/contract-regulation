import random
import string
from datetime import datetime, timedelta
import sqlite3
from pathlib import Path
import uuid

def generate_eth_address():
    # 生成随机的以太坊地址
    return '0x' + ''.join(random.choices(string.hexdigits, k=40)).lower()

def generate_rule_id():
    # 生成规则ID
    return f"RULE{datetime.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:4].upper()}"

def generate_mock_data(num_rules=50):
    # 预定义更真实的规则模板
    rule_templates = [
        {
            'name': '批量转账金额限制',
            'description': '限制 ERC20 代币批量转账时每笔交易的最大金额',
            'functions': [{
                'name': 'batchTransfer',
                'params': [{
                    'name': 'amount',
                    'type': 'uint256',
                    'condition': '<=',
                    'value': '10000000000000000000000'  # 10000 tokens with 18 decimals
                }]
            }]
        },
        {
            'name': '单笔转账限额控制',
            'description': '限制 ERC20 代币单笔转账的最大金额',
            'functions': [{
                'name': 'transfer',
                'params': [{
                    'name': 'value',
                    'type': 'uint256',
                    'condition': '<=',
                    'value': '1000000000000000000000'  # 1000 tokens with 18 decimals
                }]
            }]
        },
        {
            'name': '黑名单地址交易限制',
            'description': '禁止黑名单地址进行代币转账',
            'functions': [{
                'name': 'transfer',
                'params': [{
                    'name': 'from',
                    'type': 'address',
                    'condition': '!=',
                    'value': generate_eth_address()  # 模拟黑名单地址
                }]
            }]
        },
        {
            'name': '合约状态监控',
            'description': '监控合约状态变化，确保余额不超过限制',
            'functions': [{
                'name': 'balanceOf',
                'params': [{
                    'name': 'balance',
                    'type': 'uint256',
                    'condition': '<=',
                    'value': '100000000000000000000000'  # 100000 tokens with 18 decimals
                }]
            }]
        }
    ]
    
    owners = ['admin', 'operator', 'supervisor', 'auditor', 'manager']
    
    # 获取数据库路径
    db_path = Path(__file__).parent.parent / 'instance' / 'ethregulation.db'
    
    print(f"Connecting to database: {db_path}")
    
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # 生成规则数据
        for i in range(num_rules):
            # 随机选择一个规则模板
            template = random.choice(rule_templates)
            
            # 插入规则
            rule_data = {
                'name': f"{template['name']}_{i+1}",
                'regulator_address': generate_eth_address(),
                'description': template['description'],
                'contract_address': generate_eth_address(),
                'owner': random.choice(owners),
                'rule_id': generate_rule_id(),
                'status': random.randint(0, 2),  # 0: 待审核, 1: 已上线, 2: 已下线
                'create_time': (datetime.now() - timedelta(days=random.randint(0, 60))).strftime('%Y-%m-%d %H:%M:%S')
            }
            
            cursor.execute('''
                INSERT INTO rules (name, regulator_address, description, contract_address, 
                                 owner, rule_id, status, create_time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                rule_data['name'],
                rule_data['regulator_address'],
                rule_data['description'],
                rule_data['contract_address'],
                rule_data['owner'],
                rule_data['rule_id'],
                rule_data['status'],
                rule_data['create_time']
            ))
            
            rule_id = cursor.lastrowid
            
            # 添加函数和参数
            for func in template['functions']:
                cursor.execute('''
                    INSERT INTO rule_functions (rule_id, name)
                    VALUES (?, ?)
                ''', (rule_id, func['name']))
                
                function_id = cursor.lastrowid
                
                for param in func['params']:
                    cursor.execute('''
                        INSERT INTO rule_parameters (function_id, name, type, condition, value)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (
                        function_id,
                        param['name'],
                        param['type'],
                        param['condition'],
                        param['value']
                    ))
            
            if (i + 1) % 10 == 0:
                print(f"Added {i + 1} rules...")
        
        conn.commit()
        print(f"Successfully added {num_rules} mock rules to the database")
        
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    generate_mock_data() 