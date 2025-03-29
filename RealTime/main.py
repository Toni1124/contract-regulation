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
        
        begin_block = 17000000
        end_block = 17000001
        
        print(f"\n🎯 Target range: Block {begin_block} to {end_block}")
        processor = TransactionProcessor()
        processor.process_range(begin_block, end_block, contract_addresses)
        
    except Exception as e:
        logger.error(f"❌ Main process error: {str(e)}")
        print(f"\n❌ Program terminated with error: {str(e)}")
    else:
        print("\n✨ Program completed successfully")

if __name__ == "__main__":
    main()
