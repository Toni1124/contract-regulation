import psycopg2
from psycopg2.extras import RealDictCursor

def check_table():
    # 数据库连接配置
    conn_params = {
        'dbname': 'db',
        'user': 'ethereum',
        'password': 'emm20240809!',
        'host': '10.0.2.251',
        'port': '5432'
    }
    
    try:
        # 连接数据库
        conn = psycopg2.connect(**conn_params)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # 获取表结构
        cur.execute("""
            SELECT column_name, data_type, character_maximum_length
            FROM information_schema.columns
            WHERE table_name = 'rules_new'
            ORDER BY ordinal_position;
        """)
        columns = cur.fetchall()
        
        print("=== Table Structure ===")
        for col in columns:
            print(f"Column: {col['column_name']}")
            print(f"Type: {col['data_type']}")
            if col['character_maximum_length']:
                print(f"Length: {col['character_maximum_length']}")
            print("---")
        
        # 获取示例数据
        print("\n=== Sample Data ===")
        cur.execute("SELECT * FROM rules_new LIMIT 5")
        rows = cur.fetchall()
        for row in rows:
            print("\nRecord:")
            for key, value in row.items():
                print(f"{key}: {value}")
            print("---")
        
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    check_table() 