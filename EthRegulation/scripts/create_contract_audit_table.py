import psycopg2
from psycopg2 import Error

try:
    conn = psycopg2.connect(
        host='10.0.2.251',
        dbname='db',
        user='ethereum',
        password='emm20240809!'
    )
    cursor = conn.cursor()

    create_table_query = '''
    CREATE TABLE IF NOT EXISTS contract_audits (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        source_code TEXT NOT NULL,
        version VARCHAR(20) NOT NULL,
        submit_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        audit_status INTEGER NOT NULL DEFAULT 0,
        audit_result JSONB,
        registered_contract_id INTEGER,
        CONSTRAINT fk_registered_contract
            FOREIGN KEY(registered_contract_id)
            REFERENCES contracts(id)
            ON DELETE SET NULL,
        CONSTRAINT chk_audit_status 
            CHECK (audit_status IN (0, 1, 2))
    );

    COMMENT ON TABLE contract_audits IS '智能合约审核表';
    COMMENT ON COLUMN contract_audits.name IS '合约名称';
    COMMENT ON COLUMN contract_audits.source_code IS '合约源代码';
    COMMENT ON COLUMN contract_audits.version IS 'Solidity版本';
    COMMENT ON COLUMN contract_audits.submit_time IS '提交时间';
    COMMENT ON COLUMN contract_audits.audit_status IS '审核状态：0-待审核，1-通过，2-未通过';
    COMMENT ON COLUMN contract_audits.audit_result IS 'Slither分析结果';
    COMMENT ON COLUMN contract_audits.registered_contract_id IS '关联的已注册合约ID';
    '''

    cursor.execute(create_table_query)

    create_index_queries = [
        'CREATE INDEX idx_contract_audits_submit_time ON contract_audits(submit_time);',
        'CREATE INDEX idx_contract_audits_audit_status ON contract_audits(audit_status);',
        'CREATE INDEX idx_contract_audits_name ON contract_audits(name);'
    ]

    for query in create_index_queries:
        cursor.execute(query)

    conn.commit()
    print("Table created successfully")

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    if conn:
        cursor.close()
        conn.close()
        print("PostgreSQL connection is closed")
