import os
from datetime import timedelta

class Config:
    # Default to PostgreSQL, fallback to SQLite
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://ethereum:emm20240809!@10.0.2.251:5432/db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
    JSON_AS_ASCII = False

    # 添加新的配置
    TEMP_CONTRACT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'temp_contracts')
    SLITHER_REPORTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reports/slither')

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:' 