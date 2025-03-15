import sys, logging
sys.path.append("..") 
try:
    import config
except:
    from reglang import config

logging.basicConfig(
    level = config.LOG_LEVEL,
    format = '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)03d] %(message)s',
    datefmt = '%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)