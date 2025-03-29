import logging
import os
from datetime import datetime
from tqdm import tqdm

# 创建logs目录
LOGS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
os.makedirs(LOGS_DIR, exist_ok=True)

# 配置日志
log_file = os.path.join(LOGS_DIR, f'eth_monitor_{datetime.now().strftime("%Y%m%d")}.log')

# 创建格式化器
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')

# 文件处理器
file_handler = logging.FileHandler(log_file)
file_handler.setFormatter(formatter)

# 控制台处理器（只显示INFO及以上级别）
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.INFO)

# 配置logger
logger = logging.getLogger('eth_monitor')
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(console_handler)
