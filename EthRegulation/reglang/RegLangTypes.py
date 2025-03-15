from web3 import Web3
import redis, json, sys
sys.path.append("..") 
try:
    import config
except:
    from reglang import config
from reglang.solidity_storage import Solidity_Storage
from reglang.logger import logger

# All contracts info
class RegContracts:
    def __init__(self):
        self.contracts = {}
        # TODO: use leveldb to replace redis
        if config.REDIS_AVAILABLE:
            self.contract_pool = redis.ConnectionPool(host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.REDIS_CONTRACT_DB, decode_responses=True)

    def add_full_contract(self, addr, contractOwner, contractName, sourceCode):
        logger.debug("Adding local contract: %s (%s)" % (addr, contractName))
        self.contracts[addr] = Contract(addr, contractOwner, contractName, sourceCode)
        if config.REDIS_AVAILABLE:
            r = redis.Redis(connection_pool=self.contract_pool)
            contract_info = {"addr": addr, "contractOwner": contractOwner, "contractName": contractName, "sourceCode": sourceCode}
            r.set(addr, json.dumps(contract_info))

    
    def fetch_remote_contract(self, addr):
        logger.debug("Fetching remote contract: %s" % addr)
        if not config.REDIS_AVAILABLE:
            raise Exception("Remote contracts not available.")
        r = redis.Redis(connection_pool=self.contract_pool)
        if r.exists(addr):
            try:
                contract_info = json.loads(r.get(addr))
                assert(addr == contract_info["addr"])
            except Exception as e:
                raise Exception("Fetch remote contract error: %s"%e)
        else:
            raise Exception("Fetch remote contract error: contract does not exist(%s)"%addr)
        contract = Contract(contract_info["addr"], contract_info["contractOwner"], contract_info["contractName"], contract_info["sourceCode"])
        self.contracts[addr] = contract
        return contract

    def get_contract(self, addr):
        if addr in self.contracts.keys():
            return self.contracts[addr]
        else:
            logger.debug("Fetch remote contract: %s", addr)
            return self.fetch_remote_contract(addr)


# Single contract Object
class Contract:
    def __init__(self, addr, contractOwner, contractName, sourceCode):
        self.addr = addr
        self.contractOwner = contractOwner
        self.contractName = contractName
        self.sourceCode = sourceCode
        self.storage = Solidity_Storage(sourceCode, config.SOLC_PATH)
        self.web3Contract = Web3().eth.contract(abi=self.storage.abis[contractName], bytecode=self.storage.bytecodes[contractName])

    def get_state(self, varName, index=None):
        # TODO: deal with offset and value_size(such as uint8)
        # TODO: more types(such as address)
        contractAddr = Web3.toChecksumAddress(self.addr)
        if index is None:
            # query returns: slot,offset,value_size,types,True
            slot,offset,value_size,types,success = self.storage.query(self.contractName, [varName])
            stateIndex = hex(slot)
        else:
            slot,offset,value_size,types,success = self.storage.query(self.contractName, [varName, int(index,16)])
            stateIndex = hex(slot)
        result =  Web3(Web3.HTTPProvider(config.REMOTE_RPC)).eth.getStorageAt(contractAddr, stateIndex)
        if types == "string":
            str_result = str(result, encoding = 'utf-8')
            logger.debug("Fetch remote state(%s) %s[%s]: %s"%(types,varName,index,str_result))
            return str_result
        elif types.startswith("uint"):
            int_result = int.from_bytes(result, 'big')
            logger.debug("Fetch remote state(%s) %s[%s]: %s"%(types,varName,index,int_result))
            return int_result
        else:
            logger.warning("Fetch remote state with unkown type: %s" % types)

    

# Transaction to regulate
class RegTx:
    def __init__(self, fromAddr, toAddr, data, readSet, writeSet, contracts):
        self.fromAddr = fromAddr
        self.toAddr = toAddr
        self.originalReadSet = readSet
        self.originalWriteSet = writeSet
        self.contracts = contracts

        # decode msg.data
        self.toContract = self.contracts.get_contract(toAddr)
        tx_decode_result = self.toContract.web3Contract.decode_function_input(data)
        self.function = type(tx_decode_result[0]).__name__
        self.args = tx_decode_result[1]


# Tx readset variables
class ReadSetVar:
    def __init__(self, tx, contractAddr, varName):
        self.tx = tx
        self.contractAddr = contractAddr
        self.varName = varName

    def getValue(self, index=None):
        # TODO: deal with offset and value_size
        contract = self.tx.contracts.get_contract(self.contractAddr)
        if index is None:
            readSetIndex = hex(contract.storage.query(contract.contractName, [self.varName])[0])
        elif isinstance(index, str):
            readSetIndex = hex(contract.storage.query(contract.contractName, [self.varName, int(index,16)])[0])
        elif isinstance(index, int):
            readSetIndex = hex(contract.storage.query(contract.contractName, [self.varName, index])[0])
        else:
            logger.warning("ReadSetVar getValue failed: %s[%s]"%(self.varName, index))
        return self.tx.originalReadSet[self.contractAddr][readSetIndex]


# Tx writeset variables
class WriteSetVar:
    def __init__(self, tx, contractAddr, varName):
        self.tx = tx
        self.contractAddr = contractAddr
        self.varName = varName

    def getValue(self, index=None):
        # TODO: deal with offset and value_size
        contract = self.tx.contracts.get_contract(self.contractAddr)
        if index is None:
            writeSetIndex = hex(contract.storage.query(contract.contractName, [self.varName])[0])
        elif isinstance(index, str):
            writeSetIndex = hex(contract.storage.query(contract.contractName, [self.varName, int(index,16)])[0])
        elif isinstance(index, int):
            writeSetIndex = hex(contract.storage.query(contract.contractName, [self.varName, index])[0])
        else:
            logger.warning("WriteSetVar getValue failed: %s[%s]"%(self.varName, index))
        return self.tx.originalWriteSet[self.tx.toAddr][writeSetIndex]

# Contract state variables
class ContractStateVar:
    def __init__(self, tx, contractAddr, varName):
        self.tx = tx
        self.contractAddr = contractAddr
        self.varName = varName

    def getValue(self, index=None):
        contract = self.tx.contracts.get_contract(self.contractAddr)
        return contract.get_state(self.varName, index)
