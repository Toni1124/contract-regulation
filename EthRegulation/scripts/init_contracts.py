from app import create_app
from app.extensions import db
from app.models.contract import Contract
import random
from datetime import datetime, timedelta
import sqlalchemy as sa

def generate_address():
    # 生成随机的以太坊地址
    return '0x' + ''.join(random.choices('0123456789abcdef', k=40))

def generate_timestamp():
    # 生成最近30天内的随机时间戳
    now = datetime.now()
    days_ago = random.randint(0, 30)
    return now - timedelta(days=days_ago)

def init_contracts():
    app = create_app()
    with app.app_context():
        # 检查表是否存在，不存在则创建
        inspector = sa.inspect(db.engine)
        if 'contracts' not in inspector.get_table_names():
            Contract.__table__.create(db.engine)
            print("Created contracts table")
        
        # 检查是否已有数据
        if Contract.query.first():
            print("Contracts table already has data, skipping initialization")
            return
        
        # 读取ERC20合约源码
        with open('testdata/erc20.sol', 'r') as f:
            erc20_source = f.read()

        # 创建合约列表
        contracts = []

        # 1. 添加不同参数的ERC20代币合约
        token_configs = [
            ("USDT", "Tether USD", 6),
            ("USDC", "USD Coin", 6),
            ("DAI", "Dai Stablecoin", 18),
            ("WETH", "Wrapped Ether", 18),
            ("WBTC", "Wrapped Bitcoin", 8),
            ("UNI", "Uniswap", 18),
            ("LINK", "Chainlink", 18),
            ("AAVE", "Aave Token", 18),
            ("CRV", "Curve DAO Token", 18),
            ("COMP", "Compound", 18),
        ]

        for symbol, name, decimals in token_configs:
            contracts.append(Contract(
                name=f"{name} ({symbol})",
                address=generate_address(),
                source_code=erc20_source,
                create_time=generate_timestamp(),
                abi={
                    "functions": [
                        {"name": "transfer", "params": ["address", "uint256"]},
                        {"name": "transferFrom", "params": ["address", "address", "uint256"]},
                        {"name": "approve", "params": ["address", "uint256"]},
                        {"name": "balanceOf", "params": ["address"]},
                        {"name": "allowance", "params": ["address", "address"]},
                        {"name": "decimals", "params": []},
                        {"name": "symbol", "params": []},
                        {"name": "name", "params": []}
                    ]
                }
            ))

        # 2. 添加其他类型的合约
        other_contracts = [
            {
                "name": "Uniswap V2 Router",
                "abi": {
                    "functions": [
                        {"name": "swapExactTokensForTokens", "params": ["uint256", "uint256", "address[]", "address", "uint256"]},
                        {"name": "addLiquidity", "params": ["address", "address", "uint256", "uint256", "uint256", "uint256", "address", "uint256"]},
                        {"name": "removeLiquidity", "params": ["address", "address", "uint256", "uint256", "uint256", "address", "uint256"]}
                    ]
                }
            },
            {
                "name": "Uniswap V2 Pair",
                "abi": {
                    "functions": [
                        {"name": "swap", "params": ["uint256", "uint256", "address", "bytes"]},
                        {"name": "sync", "params": []},
                        {"name": "skim", "params": ["address"]}
                    ]
                }
            },
            {
                "name": "Aave Lending Pool",
                "abi": {
                    "functions": [
                        {"name": "deposit", "params": ["address", "uint256", "address", "uint16"]},
                        {"name": "withdraw", "params": ["address", "uint256", "address"]},
                        {"name": "borrow", "params": ["address", "uint256", "uint256", "uint16", "address"]}
                    ]
                }
            },
            {
                "name": "Compound cToken",
                "abi": {
                    "functions": [
                        {"name": "mint", "params": ["uint256"]},
                        {"name": "redeem", "params": ["uint256"]},
                        {"name": "borrow", "params": ["uint256"]}
                    ]
                }
            },
            {
                "name": "Curve 3pool",
                "abi": {
                    "functions": [
                        {"name": "add_liquidity", "params": ["uint256[3]", "uint256"]},
                        {"name": "remove_liquidity", "params": ["uint256", "uint256[3]"]},
                        {"name": "exchange", "params": ["int128", "int128", "uint256", "uint256"]}
                    ]
                }
            },
            {
                "name": "Chainlink Price Feed",
                "abi": {
                    "functions": [
                        {"name": "latestRoundData", "params": []},
                        {"name": "getAnswer", "params": ["uint256"]},
                        {"name": "getTimestamp", "params": ["uint256"]}
                    ]
                }
            },
            {
                "name": "Gnosis Safe",
                "abi": {
                    "functions": [
                        {"name": "execTransaction", "params": ["address", "uint256", "bytes", "uint8", "uint256", "uint256", "uint256", "address", "address", "bytes"]},
                        {"name": "getOwners", "params": []},
                        {"name": "getThreshold", "params": []}
                    ]
                }
            },
            {
                "name": "ENS Registry",
                "abi": {
                    "functions": [
                        {"name": "setResolver", "params": ["bytes32", "address"]},
                        {"name": "setOwner", "params": ["bytes32", "address"]},
                        {"name": "setTTL", "params": ["bytes32", "uint64"]}
                    ]
                }
            },
            {
                "name": "NFT Marketplace",
                "abi": {
                    "functions": [
                        {"name": "createSale", "params": ["address", "uint256", "uint256"]},
                        {"name": "cancelSale", "params": ["uint256"]},
                        {"name": "buyItem", "params": ["uint256"]}
                    ]
                }
            },
            {
                "name": "Yield Farming",
                "abi": {
                    "functions": [
                        {"name": "stake", "params": ["uint256"]},
                        {"name": "withdraw", "params": ["uint256"]},
                        {"name": "getReward", "params": []}
                    ]
                }
            }
        ]

        # 为其他类型合约生成示例源码和地址
        for contract_info in other_contracts:
            contract_source = f"""
            // SPDX-License-Identifier: MIT
            pragma solidity ^0.8.0;

            contract {contract_info['name'].replace(' ', '')} {{
                // 这里是 {contract_info['name']} 的示例实现
                // 实际合约功能比这个复杂得多
                
                address public owner;
                
                constructor() {{
                    owner = msg.sender;
                }}
                
                // 实现的函数
                {chr(10).join([f'function {func["name"]}({", ".join([f"_{i} {p}" for i, p in enumerate(func["params"])])}) public {{}}' for func in contract_info['abi']['functions']])}
            }}
            """
            
            contracts.append(Contract(
                name=contract_info['name'],
                address=generate_address(),
                source_code=contract_source,
                create_time=generate_timestamp(),
                abi=contract_info['abi']
            ))

        try:
            # 批量添加所有合约
            db.session.add_all(contracts)
            db.session.commit()
            print(f"Successfully initialized {len(contracts)} contracts")
        except Exception as e:
            db.session.rollback()
            print(f"Error initializing contracts: {e}")
            raise

if __name__ == '__main__':
    init_contracts() 