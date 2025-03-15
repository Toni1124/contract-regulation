from flask import Blueprint, request, jsonify
import os
from reglang import RegContracts, RegTx, RegLang
from typing import Dict, Any, Tuple

bp = Blueprint('reglang', __name__)

# Helper function to read contract or rl files if they are provided as filenames.
def read_file(filename: str) -> str:
    path = os.path.join("testdata", filename)
    with open(path, 'r') as file:
        return file.read()

@bp.route('/reglang', methods=['POST'])
def regulate_contract() -> Tuple[Dict[str, Any], int]:
    data = request.get_json()
    if not data:
        return {
            'code': 400,
            'message': 'No input data provided'
        }, 400

    try:
        # Extract contracts_info, txs_info, rl_files, contract_files from request
        contracts_info = data.get("contracts_info", {})
        txs_info = data.get("txs_info", {})
        rl_files = data.get("rl_files", {})
        contract_files = data.get("contract_files", {})

        # Set up contracts
        contracts = RegContracts()
        for contract_name, contract_data in contracts_info.items():
            addr = contract_data["addr"]
            owner = contract_data["contractOwner"]
            name = contract_data["contractName"]
            source_code = contract_data.get("sourceCode") or read_file(contract_files.get(contract_name))
            contracts.add_full_contract(addr, owner, name, source_code)

        # Initialize transaction
        tx_info = txs_info.get("batchTransfer", {})
        tx = RegTx(
            tx_info["from"],
            tx_info["to"],
            tx_info["data"],
            tx_info.get("readSet", {}),
            tx_info.get("writeSet", {}),
            contracts
        )

        # Evaluate each rl file against the transaction
        results = {}
        for rl_name, rl_content in rl_files.items():
            rl_code = rl_content or read_file(rl_name)
            regulation_result = RegLang(rl_code, tx).regulate()
            results[rl_name] = regulation_result

        return {
            'code': 200,
            'message': 'success',
            'data': results
        }, 200

    except Exception as e:
        return {
            'code': 400,
            'message': str(e)
        }, 400 