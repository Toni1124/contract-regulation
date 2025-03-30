from transaction_processor import TransactionProcessor

# 重新检查所有交易
processor = TransactionProcessor()
processor.recheck_existing_transactions()

# 或者只重新检查特定合约的交易
contract_addresses = ['0xdAC17F958D2ee523a2206206994597C13D831ec7']
processor.recheck_existing_transactions(contract_addresses)
