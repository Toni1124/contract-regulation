from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import create_app, db
import sqlite3
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_sqlite_schema():
    """获取 SQLite 数据库的表结构"""
    sqlite_conn = sqlite3.connect('instance/ethregulation.db')
    sqlite_cursor = sqlite_conn.cursor()
    
    sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = sqlite_cursor.fetchall()
    
    schema = {}
    for table in tables:
        table_name = table[0]
        sqlite_cursor.execute(f"PRAGMA table_info({table_name})")
        columns = sqlite_cursor.fetchall()
        schema[table_name] = columns
        logger.info(f"\nTable: {table_name}")
        for col in columns:
            logger.info(f"Column: {col}")
    
    sqlite_conn.close()
    return schema

def get_sqlite_data():
    """获取 SQLite 数据库的数据"""
    sqlite_conn = sqlite3.connect('instance/ethregulation.db')
    sqlite_cursor = sqlite_conn.cursor()
    
    sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = sqlite_cursor.fetchall()
    
    data = {}
    for table in tables:
        table_name = table[0]
        if table_name != 'alembic_version':
            sqlite_cursor.execute(f"SELECT * FROM {table_name}")
            rows = sqlite_cursor.fetchall()
            data[table_name] = rows
            
            sqlite_cursor.execute(f"PRAGMA table_info({table_name})")
            data[f"{table_name}_columns"] = [column[1] for column in sqlite_cursor.fetchall()]
            
            logger.info(f"\nTable {table_name} has {len(rows)} rows")
            if rows:
                logger.info(f"Sample row: {rows[0]}")
    
    sqlite_conn.close()
    return data

def clear_postgres_tables(pg_cursor):
    """清空 PostgreSQL 中的所有表数据"""
    tables = ['rules', 'rule_functions', 'rule_parameters', 'contracts']
    for table in tables:
        try:
            pg_cursor.execute(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE;")
            logger.info(f"Cleared table: {table}")
        except Exception as e:
            logger.warning(f"Could not clear table {table}: {str(e)}")

def migrate_to_postgres():
    # 获取数据
    logger.info("\nReading data from SQLite...")
    sqlite_data = get_sqlite_data()
    
    # 连接 PostgreSQL
    logger.info("\nConnecting to PostgreSQL...")
    pg_conn = psycopg2.connect(
        host='10.0.2.251',
        dbname='db',
        user='ethereum',
        password='emm20240809!'
    )
    pg_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    pg_cursor = pg_conn.cursor()
    
    # 创建 Flask app context
    app = create_app()
    with app.app_context():
        logger.info("\nDropping and recreating all tables...")
        db.drop_all()  # 删除所有表
        db.create_all()  # 重新创建所有表
        
        # 检查创建的表
        pg_cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema='public'
        """)
        pg_tables = [table[0] for table in pg_cursor.fetchall()]
        logger.info(f"\nCreated PostgreSQL tables: {pg_tables}")
        
        # 迁移数据
        for table_name in sqlite_data:
            if not table_name.endswith('_columns'):
                try:
                    columns = sqlite_data[f"{table_name}_columns"]
                    columns_str = ', '.join(columns)
                    placeholders = ', '.join(['%s'] * len(columns))
                    
                    logger.info(f"\nMigrating data for table: {table_name}")
                    for row in sqlite_data[table_name]:
                        query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"
                        try:
                            pg_cursor.execute(query, row)
                            logger.info(f"Successfully inserted row into {table_name}")
                        except Exception as e:
                            logger.error(f"Error inserting into {table_name}: {str(e)}")
                except Exception as e:
                    logger.error(f"Error processing table {table_name}: {str(e)}")
    
    pg_conn.close()

if __name__ == '__main__':
    try:
        migrate_to_postgres()
        logger.info("\nMigration completed successfully")
    except Exception as e:
        logger.error(f"\nMigration failed: {str(e)}") 