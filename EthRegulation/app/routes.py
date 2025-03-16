from flask import Blueprint, request, jsonify
from app.models import Rule
from app import db

bp = Blueprint('api', __name__)

@bp.route('/rules/<int:id>', methods=['PUT'])
def update_rule(id):
    try:
        rule = Rule.query.get_or_404(id)
        data = request.get_json()
        
        # 更新规则数据
        rule.name = data.get('name', rule.name)
        rule.contract_address = data.get('contractAddress', rule.contract_address)
        rule.description = data.get('description', rule.description)
        # 更新其他字段...
        
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'message': 'Rule updated successfully',
            'data': rule.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 400,
            'message': str(e)
        }), 400 