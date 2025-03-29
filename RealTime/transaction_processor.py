import psycopg2
from concurrent.futures import ThreadPoolExecutor
from config import DB_CONFIG, BATCH_SIZE, MAX_WORKERS
from abi_manager import ABIManager
from logger import logger
from tqdm import tqdm
import time
import json

class TransactionProcessor:
    def __init__(self):
        self.abi_manager = ABIManager()
        
    def process_batch(self, start_block, end_block, contract_addresses):
        batch_start_time = time.time()
        conn = None
        try:
            print(f"\n📦 Processing batch: {start_block} -> {end_block}")
            conn = psycopg2.connect(**DB_CONFIG)
            
            # 获取原始交易数据
            with conn.cursor() as cursor:
                query = """
                SELECT * FROM "default".eth_transaction
                WHERE block_number BETWEEN %s AND %s
                AND to_address = ANY(%s)
                ORDER BY block_number, transaction_index
                """
                
                cursor.execute(query, (start_block, end_block, contract_addresses))
                transactions = cursor.fetchall()
                
                if not transactions:
                    print(f"ℹ️ No transactions found in blocks {start_block}-{end_block}")
                    return

                print(f"🔍 Found {len(transactions)} transactions to process")
                
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
            
            # 为每个交易创建新的游标和事务
            for tx in transactions:
                cursor = conn.cursor()
                try:
                    tx_dict = dict(zip(columns, tx))
                    
                    to_address = tx_dict.get('to_address')
                    if not to_address:
                        continue
                    
                    input_data = tx_dict.get('input')
                    if not input_data:
                        input_data = '0x'
                    
                    # 解析input数据
                    func_signature, func_name, decoded_params = self.abi_manager.decode_input(
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
                    conn.commit()  # 每个交易单独提交
                    success_count += 1
                    
                    if success_count % 10 == 0:
                        print(f"📊 Progress: {success_count} succeeded, {error_count} failed")
                    
                except Exception as e:
                    conn.rollback()  # 只回滚当前交易
                    error_count += 1
                    print(f"❌ Error processing transaction at block={tx_dict.get('block_number', 'unknown')}: {str(e)}")
                    continue
                finally:
                    cursor.close()
            
            batch_time = time.time() - batch_start_time
            print(f"\n✅ Batch completed in {batch_time:.2f}s")
            print(f"📊 Summary: {success_count} succeeded, {error_count} failed")
            
        except Exception as e:
            print(f"❌ Batch error: {str(e)}")
        finally:
            if conn:
                conn.close()

    def process_range(self, begin_block, end_block, contract_addresses):
        print(f"\n🚀 Starting processing range: {begin_block} -> {end_block}")
        
        # 计算批次
        batches = []
        current_block = begin_block
        while current_block < end_block:
            batch_end = min(current_block + BATCH_SIZE, end_block)
            batches.append((current_block, batch_end))
            current_block = batch_end + 1
        
        print(f"📑 Total batches: {len(batches)}")
        
        completed_batches = 0
        start_time = time.time()
        
        # 并行处理批次
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = [
                executor.submit(self.process_batch, start, end, contract_addresses)
                for start, end in batches
            ]
            
            # 等待所有批次完成
            for future in futures:
                try:
                    future.result()
                    completed_batches += 1
                    print(f"\n📈 Progress: {completed_batches}/{len(batches)} batches completed")
                except Exception as e:
                    logger.error(f"❌ Future execution error: {str(e)}")
                    continue
        
        total_time = time.time() - start_time
        print(f"\n🎉 Processing completed in {total_time:.2f}s")
        print(f"📊 Final summary: {completed_batches}/{len(batches)} batches completed")
