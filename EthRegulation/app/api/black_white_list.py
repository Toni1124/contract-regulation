from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.black_white_list import BlackWhiteList
from app.schemas.black_white_list import BlackWhiteListSchema
from sqlalchemy import func
from typing import Dict, Any, Tuple, Union
from datetime import datetime

bp = Blueprint('black_white_list', __name__, url_prefix='/api')
schema = BlackWhiteListSchema()

@bp.route('/black-white-list', methods=['GET'])
def get_list() -> Tuple[Dict[str, Any], int]:
    # 获取所有查询参数
    keyword = request.args.get('keyword', '')
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    type_filter = request.args.get('type', type=int)
    region = request.args.get('region')
    organization = request.args.get('organization')
    operator = request.args.get('operator')
    
    query = BlackWhiteList.query
    
    # 应用所有过滤条件
    if keyword:
        query = query.filter(
            func.lower(BlackWhiteList.address).contains(func.lower(keyword))
        )
    if type_filter:
        query = query.filter(BlackWhiteList.type == type_filter)
    if region:
        query = query.filter(BlackWhiteList.region == region)
    if organization:
        query = query.filter(BlackWhiteList.organization == organization)
    if operator:
        query = query.filter(BlackWhiteList.operator == operator)
    
    # 计算总数
    total = query.count()
    
    # 分页
    items = query.order_by(BlackWhiteList.operate_time.desc())\
        .offset((page - 1) * page_size)\
        .limit(page_size)\
        .all()
    
    return {
        'code': 200,
        'message': 'success',
        'data': {
            'list': schema.dump(items, many=True),
            'total': total,
            'page': page,
            'pageSize': page_size
        }
    }, 200

@bp.route('/black-white-list', methods=['POST'])
def create() -> Tuple[Dict[str, Any], int]:
    data = request.get_json()
    if not data:
        return {'code': 400, 'message': 'No input data provided'}, 400

    print("Received data:", data)  # 打印接收到的数据

    # 先验证数据
    errors = schema.validate(data)
    if errors:
        print("Validation errors:", errors)  # 打印验证错误
        return {
            'code': 400, 
            'message': 'Validation error', 
            'errors': errors
        }, 400

    try:
        # 创建新实例时添加操作时间
        item = BlackWhiteList(
            **data,
            operate_time=datetime.now()
        )
        db.session.add(item)
        db.session.commit()
    except Exception as e:
        print("Database error:", str(e))  # 打印数据库错误
        db.session.rollback()
        return {'code': 400, 'message': str(e)}, 400

    return {
        'code': 200,
        'message': 'success',
        'data': schema.dump(item)
    }, 200

@bp.route('/black-white-list/<int:id>', methods=['PUT'])
def update(id: int) -> Tuple[Dict[str, Any], int]:
    item = BlackWhiteList.query.get_or_404(id)
    
    data = request.get_json()
    if not data:
        return {'code': 400, 'message': 'No input data provided'}, 400

    # 只验证提供的字段
    partial_schema = BlackWhiteListSchema(partial=True)
    errors = partial_schema.validate(data)
    if errors:
        return {
            'code': 400, 
            'message': 'Validation error', 
            'errors': errors
        }, 400

    # 检查新地址是否与其他记录冲突
    if 'address' in data:
        existing = BlackWhiteList.query.filter(
            BlackWhiteList.id != id,
            func.lower(BlackWhiteList.address) == func.lower(data['address'])
        ).first()
        if existing:
            return {'code': 400, 'message': 'Address already exists'}, 400

    # 更新记录
    for key, value in data.items():
        if hasattr(item, key):  # 只更新模型中存在的字段
            setattr(item, key, value)
    
    db.session.commit()

    return {
        'code': 200,
        'message': 'success',
        'data': schema.dump(item)
    }, 200

@bp.route('/black-white-list/<int:id>', methods=['DELETE'])
def delete(id: int) -> Tuple[Dict[str, Any], int]:
    item = BlackWhiteList.query.get_or_404(id)
    
    db.session.delete(item)
    db.session.commit()

    return {
        'code': 200,
        'message': 'success'
    }, 200 