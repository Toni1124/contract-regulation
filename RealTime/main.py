import os
from config import DATA_DIR
from init_db import init_database
from transaction_processor import TransactionProcessor
from logger import logger

def read_contract_addresses():
    addresses_file = os.path.join(DATA_DIR, 'contract_addresses.txt')
    with open(addresses_file, 'r') as f:
        return [addr.strip() for addr in f.readlines() if addr.strip()]

def main():
    try:
        print("\n🔧 Initializing system...")
        init_database()
        
        contract_addresses = read_contract_addresses()
        print(f"📝 Loaded {len(contract_addresses)} contract addresses")
        
        begin_block = 17100000
        end_block = 18000000
        
        print(f"\n🎯 Target range: Block {begin_block} to {end_block}")
        processor = TransactionProcessor()
        processor.process_range(begin_block, end_block, contract_addresses)
        
    except Exception as e:
        logger.error(f"❌ Main process error: {str(e)}")
        print(f"\n❌ Program terminated with error: {str(e)}")
    else:
        print("\n✨ Program completed successfully")

def recheck_transactions(contract_addresses=None):
    processor = TransactionProcessor()
    processor.recheck_existing_transactions(contract_addresses)

if __name__ == "__main__":
    # 示例1：重新检查所有交易
    #recheck_transactions()
    main()
    # 示例2：只重新检查指定合约的交易
    # contract_addresses = ['0xdAC17F958D2ee523a2206206994597C13D831ec7']
    # recheck_transactions(contract_addresses)
