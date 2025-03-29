import json
import os
import requests
from web3 import Web3
from eth_utils import encode_hex
from hexbytes import HexBytes
from config import ABI_DIR

class ABIManager:
    def __init__(self):
        self.etherscan_api_key = "A96UUWIMH23K4EI5AKNVBZ8SYKZQ2BGT1X"
        self.abi_cache = {}
        self.w3 = Web3()

    def get_abi(self, contract_address):
        try:
            # 首先检查缓存
            if contract_address in self.abi_cache:
                return self.abi_cache[contract_address]

            # 检查本地文件
            abi_file = os.path.join('abis', f"{contract_address.lower()}.json")
            if os.path.exists(abi_file):
                with open(abi_file, 'r') as f:
                    abi = json.load(f)
                    self.abi_cache[contract_address] = abi
                    return abi

            print(f"🔍 Getting ABI from Etherscan for {contract_address}")
            # 从Etherscan获取ABI
            url = f"https://api.etherscan.io/api?module=contract&action=getabi&address={contract_address}&apikey={self.etherscan_api_key}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if data["status"] == "1" and data["message"] == "OK":
                    abi = json.loads(data["result"])
                    
                    # 保存到本地文件
                    os.makedirs('abis', exist_ok=True)
                    with open(abi_file, 'w') as f:
                        json.dump(abi, f, indent=2)
                    
                    self.abi_cache[contract_address] = abi
                    print(f"✅ Successfully retrieved and cached ABI for {contract_address}")
                    return abi
                else:
                    print(f"❌ Etherscan API error: {data.get('message', 'Unknown error')}")
            
            print(f"❌ Failed to get ABI for contract {contract_address}")
            return None

        except Exception as e:
            print(f"❌ Error in get_abi: {str(e)}")
            return None

    def decode_input(self, contract_address, input_data):
        try:
            if not input_data or input_data == '0x':
                print(f"⚠️ Empty input data for contract {contract_address}")
                return None, None, None

            # 打印原始input数据
            print(f"\n原始input数据: {input_data}")
            
            # 确保input_data是以0x开头的十六进制字符串
            if not input_data.startswith('0x'):
                input_data = '0x' + input_data

            # 获取函数选择器（前4个字节，包含0x前缀）
            function_selector = input_data[:10]
            print(f"函数选择器: {function_selector}")

            # 获取ABI
            abi = self.get_abi(contract_address)
            if not abi:
                return None, None, None

            # 创建合约实例
            contract = self.w3.eth.contract(address=contract_address, abi=abi)

            # 直接尝试解码
            try:
                decoded = contract.decode_function_input(input_data)
                func_obj, params = decoded
                
                processed_params = {}
                for key, value in params.items():
                    if isinstance(value, (bytes, HexBytes)):
                        processed_params[key] = encode_hex(value)
                    elif isinstance(value, int):
                        processed_params[key] = str(value)
                    else:
                        processed_params[key] = value

                # 获取函数名
                func_name = func_obj.fn_name
                
                return function_selector, func_name, processed_params

            except Exception as e:
                print(f"解码错误: {str(e)}")
                return None, None, None

        except Exception as e:
            print(f"❌ Error in decode_input: {str(e)}")
            return None, None, None
