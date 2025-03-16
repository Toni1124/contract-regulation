from flask import Blueprint, request, jsonify
from app.models.rule_new import RuleNew  # 导入新模型
from app.schemas.rule_new import RuleNewSchema  # 导入新Schema
from app.extensions import db
from datetime import datetime
import logging

# 设置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

bp = Blueprint('rules', __name__)
rule_schema = RuleNewSchema()
rules_schema = RuleNewSchema(many=True)

@bp.route('/api/rules', methods=['GET'])
def get_rules():
    logger.debug("Fetching rules from rules_new table")
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    keyword = request.args.get('keyword', '')
    
    query = RuleNew.query
    if keyword:
        query = query.filter(
            (RuleNew.name.ilike(f'%{keyword}%')) |
            (RuleNew.contract_address.ilike(f'%{keyword}%'))
        )
    
    total = query.count()
    items = query.order_by(RuleNew.id.desc())\
        .offset((page - 1) * page_size)\
        .limit(page_size)\
        .all()
    
    logger.debug(f"Found {total} rules")
    return {
        'code': 200,
        'message': 'success',
        'data': {
            'list': rules_schema.dump(items),
            'total': total,
            'page': page,
            'pageSize': page_size
        }
    }

@bp.route('/api/rules', methods=['POST'])
def create_rule():
    try:
        data = request.get_json()
        rule = RuleNew(
            name=data['name'],
            contract_address=data['contractAddress'],
            description=data.get('description'),
            owner=data['owner'],
            functions=data['functions'],  # 直接存储JSON
            regulator_address=data.get('regulatorAddress')
        )
        
        db.session.add(rule)
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'message': 'success',
            'data': rule_schema.dump(rule)
        })
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating rule: {str(e)}")
        return jsonify({
            'code': 400,
            'message': str(e)
        }), 400

@bp.route('/api/rules/<int:id>', methods=['PUT'])
def update_rule(id):
    try:
        rule = RuleNew.query.get_or_404(id)
        data = request.get_json()
        
        rule.name = data.get('name', rule.name)
        rule.description = data.get('description', rule.description)
        rule.contract_address = data.get('contractAddress', rule.contract_address)
        rule.functions = data.get('functions', rule.functions)
        rule.regulator_address = data.get('regulatorAddress', rule.regulator_address)
        
        db.session.commit()
        return jsonify({
            'code': 200,
            'message': 'success',
            'data': rule_schema.dump(rule)
        })
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating rule: {str(e)}")
        return jsonify({
            'code': 400,
            'message': str(e)
        }), 400

@bp.route('/api/rules/<int:id>', methods=['DELETE'])
def delete_rule(id):
    try:
        rule = RuleNew.query.get_or_404(id)
        db.session.delete(rule)
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'message': 'success'
        })
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting rule: {str(e)}")
        return jsonify({
            'code': 400,
            'message': str(e)
        }), 400 