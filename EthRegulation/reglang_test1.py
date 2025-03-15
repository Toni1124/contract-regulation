import os
import requests
import json

def read_example(filename):
    path = os.path.join("testdata", filename)
    with open(path, 'r') as file:
        return file.read()

if __name__ == '__main__':
    # 合约信息
    contracts_info = {
        "erc20.sol": {
            "addr": "0xD1AaC31f34Ca1e5e64Ac9710DC8a59EEFabC1474",
            "contractOwner": "0x84C7768aC1Cd6d07FCA1e2BC4C3551510F6E4ABC",
            "contractName": "EIP20",
            "sourceCode": read_example("erc20.sol")
        }
    }

    # 交易信息
    txs_info = {
        "batchTransfer": {
            "from": "0x84C7768aC1Cd6d07FCA1e2BC4C3551510F6E4ABC",
            "to": "0xD1AaC31f34Ca1e5e64Ac9710DC8a59EEFabC1474",
            "data": "0x83f12fec000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000186a000000000000000000000000000000000000000000000000000000000000000020000000000000000000000005929eba30850986de6f93397a86f9b80901896e8000000000000000000000000ab8483f64d9c6d1ecf9b849ae677dd3315835cb2",
            "readSet": {
                "0xD1AaC31f34Ca1e5e64Ac9710DC8a59EEFabC1474":{
                    "0x197b7f4442862bd651f49aa6256f2e268835f42a82c8daa336e3c15f4837830f": "0x0000000000000000000000000000000000000000000000000000000000989680",
                    "0x9d4d959825f0680278e64197773b2a50cd78b2b2cb00711ddbeebf0bf93cd8a4": "0x0000000000000000000000000000000000000000000000000000000000000000",
                    "0xb25d917326bbb11780c75cb17c3902fdd3325bcfb75eb4c1d2e41d8fabe4a26c": "0x0000000000000000000000000000000000000000000000000000000000000000"
                }
            },
            "writeSet": {
                "0xD1AaC31f34Ca1e5e64Ac9710DC8a59EEFabC1474":{
                    "0x197b7f4442862bd651f49aa6256f2e268835f42a82c8daa336e3c15f4837830f": "0x0000000000000000000000000000000000000000000000000000000000958940",
                    "0x9d4d959825f0680278e64197773b2a50cd78b2b2cb00711ddbeebf0bf93cd8a4": "0x00000000000000000000000000000000000000000000000000000000000186a0",
                    "0xb25d917326bbb11780c75cb17c3902fdd3325bcfb75eb4c1d2e41d8fabe4a26c": "0x00000000000000000000000000000000000000000000000000000000000186a0"
                }
            }
        }
    }

    # .rl 文件内容
    rl_files = {
        "example1.rl": read_example("example1.rl"),
        "example2.rl": read_example("example2.rl"),
        "example3.rl": read_example("example3.rl"),
        "example4.rl": read_example("example4.rl"),
        "example5.rl": read_example("example5.rl"),
        "example6.rl": read_example("example6.rl"),
        "example7.rl": read_example("example7.rl"),
        "example8.rl": read_example("example8.rl")
    }

    # 请求数据准备
    data = {
        "contracts_info": contracts_info,
        "txs_info": txs_info,
        "rl_files": rl_files
    }

    # 发送 POST 请求到 Flask 服务
    url = 'http://127.0.0.1:5000/reglang/api'
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # 处理响应
    if response.status_code == 200:
        print("Regulate Results:")
        results = response.json().get("results", {})
        print(results)
        
    else:
        print("Request failed with status code:", response.status_code)
        print("Response:", response.text)
