from flask import Flask, request, jsonify
import os, logging
from reglang import RegContracts, RegTx, RegLang

app = Flask(__name__)

# Helper function to read contract or rl files if they are provided as filenames.
def read_file(filename):
    path = os.path.join("testdata", filename)
    with open(path, 'r') as file:
        return file.read()

@app.route('/reglang/api', methods=['POST'])
def regulate_contract():
    data = request.json

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

    return jsonify(results=results)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
