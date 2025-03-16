from flask import Blueprint, request, jsonify
from app.models.rule import Rule, RuleFunction, RuleParameter
from app.schemas.rule import RuleSchema
from app.extensions import db
from datetime import datetime
import uuid
from sqlalchemy.orm import joinedload
import json

bp = Blueprint('rules', __name__, url_prefix='/api')
rule_schema = RuleSchema()
rules_schema = RuleSchema(many=True)

@bp.route('/rules', methods=['GET'])
def get_rules():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    keyword = request.args.get('keyword', '')
    
    query = Rule.query
    
    if keyword:
        query = query.filter(Rule.name.ilike(f'%{keyword}%'))
    
    total = query.count()
    items = query.order_by(Rule.id.desc())\
        .offset((page - 1) * page_size)\
        .limit(page_size)\
        .all()
    
    return {
        'code': 200,
        'message': 'success',
        'data': {
            'list': rule_schema.dump(items, many=True),
            'total': total,
            'page': page,
            'pageSize': page_size
        }
    }

@bp.route('/rules', methods=['POST'])
def create_rule():
    try:
        data = request.get_json()  # 改为使用 JSON
        rule_data = rule_schema.load(data)
        rule_id = f"RULE{datetime.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:4].upper()}"
        
        rule = Rule(
            name=rule_data['name'],
            regulator_address=rule_data['regulator_address'],
            description=rule_data.get('description'),
            contract_address=rule_data['contract_address'],
            owner=rule_data['owner'],
            rule_id=rule_id
        )
        
        for func_data in data['functions']:
            function = RuleFunction(name=func_data['name'])
            for param_data in func_data.get('params', []):
                parameter = RuleParameter(
                    name=param_data['name'],
                    type=param_data['type'],
                    condition=param_data['condition'],
                    value=param_data['value']
                )
                function.params.append(parameter)
            rule.functions.append(function)
        
        db.session.add(rule)
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'message': 'success',
            'data': rule_schema.dump(rule)
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 400,
            'message': str(e)
        }), 400

@bp.route('/rules/<int:id>', methods=['PUT'])
def update_rule(id):
    try:
        rule = Rule.query.get_or_404(id)
        data = request.get_json()
        
        # 更新基本信息
        rule.name = data.get('name', rule.name)
        rule.description = data.get('description', rule.description)
        rule.contract_address = data.get('contractAddress', rule.contract_address)
        
        # 处理函数更新
        if 'functions' in data:
            # 使用 SQL 直接删除参数和函数，避免外键约束问题
            with db.session.begin_nested():
                # 先删除参数
                db.session.execute(
                    'DELETE FROM rule_parameters WHERE function_id IN '
                    '(SELECT id FROM rule_functions WHERE rule_id = :rule_id)',
                    {'rule_id': rule.id}
                )
                
                # 再删除函数
                db.session.execute(
                    'DELETE FROM rule_functions WHERE rule_id = :rule_id',
                    {'rule_id': rule.id}
                )
                
                # 重置序列到当前最大值
                db.session.execute(
                    "SELECT setval('rule_functions_id_seq', COALESCE((SELECT MAX(id) FROM rule_functions), 0))"
                )
                db.session.execute(
                    "SELECT setval('rule_parameters_id_seq', COALESCE((SELECT MAX(id) FROM rule_parameters), 0))"
                )
                
                # 重新创建函数和参数
                for func_data in data['functions']:
                    # 创建新函数并获取其ID
                    result = db.session.execute(
                        'INSERT INTO rule_functions (rule_id, name) VALUES (:rule_id, :name) RETURNING id',
                        {
                            'rule_id': rule.id,
                            'name': func_data['name']
                        }
                    )
                    function_id = result.scalar()
                    
                    # 创建该函数的所有参数
                    for param_data in func_data.get('params', []):
                        db.session.execute(
                            'INSERT INTO rule_parameters (function_id, name, type, condition, value) '
                            'VALUES (:function_id, :name, :type, :condition, :value)',
                            {
                                'function_id': function_id,
                                'name': param_data['name'],
                                'type': param_data['type'],
                                'condition': param_data['condition'],
                                'value': param_data['value']
                            }
                        )
        
        db.session.commit()
        return jsonify({'code': 200, 'message': 'Rule updated successfully'})
        
    except Exception as e:
        db.session.rollback()
        print(f"Error updating rule: {str(e)}")
        return jsonify({'code': 400, 'message': str(e)}), 400

@bp.route('/rules/<int:id>', methods=['DELETE'])
def delete_rule(id):
    try:
        rule = Rule.query.get_or_404(id)
        db.session.delete(rule)
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'message': 'success'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 400,
            'message': str(e)
        }), 400 