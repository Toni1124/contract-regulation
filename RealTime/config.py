import os

DB_CONFIG = {
    'host': '10.0.2.251',
    'dbname': 'db',
    'user': 'ethereum',
    'password': 'emm20240809!'
}

# 项目根目录

ABI_DIR = 'abi'
DATA_DIR = 'data'

# 确保目录存在
os.makedirs(ABI_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

BATCH_SIZE = 10000  # 每个批次处理的区块数
MAX_WORKERS = 4     # 并行处理的工作线程数
