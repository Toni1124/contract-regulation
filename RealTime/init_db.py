import psycopg2
from config import DB_CONFIG

def init_database():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    # 创建交易详情表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS eth_transaction_details (
        block_number bigint NOT NULL,
        block_timestamp timestamp without time zone NOT NULL,
        transaction_index bigint NOT NULL,
        value numeric,
        gas bigint,
        gas_price bigint,
        nonce bigint NOT NULL,
        from_address character(42) NOT NULL,
        to_address character(42),
        receipt_contract_address character(42),
        receipt_root character(66),
        block_hash character(66) NOT NULL,
        input text,
        blob_versioned_hashes character(66),
        hash character(66) NOT NULL,
        function_signature character varying(100),
        function_name character varying(100),
        decoded_parameters jsonb,
        PRIMARY KEY (block_number, transaction_index)
    )
    """)

    # 创建合约规则表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contract_rules (
        rule_id SERIAL PRIMARY KEY,
        contract_address character(42) NOT NULL,
        function_name character varying(100) NOT NULL,
        rule_type character varying(50) NOT NULL,
        rule_config jsonb NOT NULL,
        active boolean DEFAULT true,
        created_at timestamp DEFAULT CURRENT_TIMESTAMP,
        updated_at timestamp DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_contract_rules_address 
    ON contract_rules(contract_address)
    """)

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    init_database()
