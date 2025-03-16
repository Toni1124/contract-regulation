from flask import Blueprint, request, jsonify
from app.models.rule_new import RuleNew  # 导入新模型
from app.schemas.rule_new import RuleNewSchema  # 导入新Schema
from app.extensions import db
from datetime import datetime
import logging
import random
from time import sleep

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
        
        # 获取当前时间
        current_time = datetime.now()
        year = current_time.strftime('%y')
        timestamp = current_time.strftime('%H%M')
        date_key = current_time.strftime('%Y%m%d')
        
        # 获取合约地址后4位
        contract_address = data['contractAddress']
        contract_suffix = contract_address[-4:] if contract_address else 'XXXX'
        
        # 获取当天最大序号
        today_rules = RuleNew.query.filter(
            db.func.date(RuleNew.create_time) == db.func.date(current_time)
        ).all()
        sequence = str(len(today_rules) + 1).zfill(3)
        
        # 生成规则编号: R-年份-合约后4位-时间戳-序号
        rule_number = f"R-{year}-{contract_suffix}-{timestamp}-{sequence}"
        
        # 创建新规则
        rule = RuleNew(
            name=data['name'],
            contract_address=contract_address,
            description=data.get('description'),
            owner=data['owner'],
            functions=data['functions'],
            regulator_address=data.get('regulatorAddress'),
            rule_number=rule_number,  # 设置新的规则编号
            create_time=current_time
        )
        
        db.session.add(rule)
        db.session.commit()
        
        # 使用 schema 序列化数据返回给前端
        result = rule_schema.dump(rule)
        
        return jsonify({
            'code': 200,
            'message': 'success',
            'data': result  # 返回完整的规则数据，包含新生成的规则编号
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