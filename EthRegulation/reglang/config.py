# Inactived when there is another config file in parent folder.
import logging

# RegLang version
VERSION = "v1.0.0"

# Global log level
LOG_LEVEL = logging.DEBUG

# Solidity compiler path, v0.5.13 recommended
#SOLC_PATH = "C:\solc\solc.exe"
SOLC_PATH="/root/.solc-select/artifacts/solc-0.8.4/solc-0.8.4"

# ETH HTTP Provider
REMOTE_RPC = "https://ropsten.infura.io/v3/f005a211e84a455b9e25b7d2ffc7a09d"

# Redis config
REDIS_AVAILABLE = False
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_CONTRACT_DB = 0
# REDIS_REGLANG_KNOWLEDGE_DB = 1
# REDIS_REGLANG_RULE_DB = 2