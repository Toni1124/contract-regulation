from flask import Blueprint, jsonify
from app.models.contract import Contract
from app.schemas.contract import ContractSchema

bp = Blueprint('contracts', __name__)
contract_schema = ContractSchema()
contracts_schema = ContractSchema(many=True)

@bp.route('/contracts', methods=['GET'])
def get_contracts():
    contracts = Contract.query.all()
    return jsonify({
        'code': 200,
        'message': 'success',
        'data': {
            'list': contracts_schema.dump(contracts),
            'total': len(contracts)
        }
    })

@bp.route('/contracts/<address>', methods=['GET'])
def get_contract(address):
    contract = Contract.query.filter_by(address=address).first_or_404()
    return jsonify({
        'code': 200,
        'message': 'success',
        'data': contract_schema.dump(contract)
    }) 