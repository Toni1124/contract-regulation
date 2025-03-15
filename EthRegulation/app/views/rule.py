from flask import Blueprint, request, jsonify
from app.models.rule import Rule, RuleFunction, RuleParameter
from app.schemas.rule import RuleSchema
from app.extensions import db
from datetime import datetime
import uuid
from sqlalchemy.orm import joinedload
import json

bp = Blueprint('rule', __name__)
rule_schema = RuleSchema()
rules_schema = RuleSchema(many=True)

@bp.route('/rules', methods=['GET'])
def get_rules():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    keyword = request.args.get('keyword', '')

    query = Rule.query
    if keyword:
        query = query.filter(Rule.name.ilike(f'%{keyword}%') | 
                           Rule.contract_address.ilike(f'%{keyword}%'))

    # 使用 joinedload 预加载所有关联数据
    query = query.options(
        joinedload(Rule.functions).joinedload(RuleFunction.params)
    )

    pagination = query.paginate(page=page, per_page=page_size)
    rules = pagination.items
    
    # 序列化数据，确保包含所有关联数据
    result = []
    for rule in rules:
        rule_data = {
            'id': rule.id,
            'name': rule.name,
            'regulatorAddress': rule.regulator_address,
            'description': rule.description,
            'contractAddress': rule.contract_address,
            'owner': rule.owner,
            'ruleId': rule.rule_id,
            'status': rule.status,
            'createTime': rule.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'functions': []
        }
        
        for func in rule.functions:
            function_data = {
                'name': func.name,
                'params': [{
                    'name': param.name,
                    'type': param.type,
                    'condition': param.condition,
                    'value': param.value
                } for param in func.params]
            }
            rule_data['functions'].append(function_data)
            
        result.append(rule_data)

    return jsonify({
        'code': 200,
        'message': 'success',
        'data': {
            'list': result,
            'total': pagination.total
        }
    })

@bp.route('/rules', methods=['POST'])
def create_rule():
    try:
        data = request.form.to_dict()
        functions_str = request.form.get('functions', '[]')
        data['functions'] = json.loads(functions_str)
        
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
        data = request.form.to_dict()
        data['functions'] = request.json.get('functions', []) if request.is_json else []
        
        # 验证并反序列化数据
        rule_data = rule_schema.load(data, partial=True)
        
        # 更新基本信息
        for key, value in rule_data.items():
            if key != 'functions':
                setattr(rule, key, value)
        
        # 更新函数和参数
        if 'functions' in rule_data:
            # 删除旧的函数和参数
            for function in rule.functions:
                db.session.delete(function)
            
            # 添加新的函数和参数
            for func_data in rule_data['functions']:
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