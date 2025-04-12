from flask import Blueprint, request, jsonify, current_app
import os
import json
from datetime import datetime
from app.extensions import db
from app.models.contract_audit import ContractAudit
from app.models.contract import Contract
from app.schemas.contract_audit import ContractAuditSchema
from app.utils.slither_analyzer import SlitherAnalyzer
import logging

# 设置日志
logging.basicConfig(
    filename='logs/contract_audit.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

bp = Blueprint('contract_audit', __name__, url_prefix='/api/contract-audit')
analyzer = None  # 初始化为 None
schema = ContractAuditSchema()

def get_analyzer():
    global analyzer
    if analyzer is None:
        analyzer = SlitherAnalyzer()
    return analyzer

def format_description(description: str) -> str:
    """格式化描述文本，保持原有的换行和缩进"""
    return description.strip()

@bp.route('/submit', methods=['POST'])
def submit_audit():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'code': 400, 'message': 'No input data provided'}), 400

        # 保存合约代码到临时文件
        temp_dir = current_app.config['TEMP_CONTRACT_DIR']
        os.makedirs(temp_dir, exist_ok=True)
        
        contract_filename = f"contract_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sol"
        contract_path = os.path.join(temp_dir, contract_filename)
        
        with open(contract_path, 'w') as f:
            f.write(data['source_code'])

        # 运行Slither分析
        analyzer = get_analyzer()
        analysis_result = analyzer.analyze_contract(contract_path)
        
        if not analysis_result['success']:
            logger.error(f"Analysis failed: {analysis_result['error']}")
            return jsonify({
                'code': 500,
                'message': 'Contract analysis failed',
                'data': {
                    'success': False,
                    'error': analysis_result['error']
                }
            }), 500

        # 读取Slither报告
        with open(analysis_result['output_file'], 'r') as f:
            slither_report = json.load(f)

        # 过滤出高危漏洞
        high_severity_issues = []
        for detector in slither_report.get('results', {}).get('detectors', []):
            if detector['impact'] == 'High':
                high_severity_issues.append({
                    'title': detector['check'],
                    'severity': detector['impact'].lower(),
                    'description': format_description(detector['description']),
                    'check': detector['check'],
                    'confidence': detector['confidence'],
                    'location': {
                        'line': detector.get('elements', [{}])[0].get('source_mapping', {}).get('lines', [0])[0],
                        'code': detector.get('elements', [{}])[0].get('source_mapping', {}).get('content', '').strip()
                    } if detector.get('elements') else None
                })

        # 确定审核结果
        audit_passed = len(high_severity_issues) == 0

        # 创建审核记录
        contract_audit = ContractAudit(
            name=data['name'],
            source_code=data['source_code'],
            version=data['version'],
            audit_status=1 if audit_passed else 2,
            audit_result={
                'securityChecks': high_severity_issues
            } if high_severity_issues else None
        )
        
        db.session.add(contract_audit)
        db.session.commit()

        return jsonify({
            'code': 200,
            'message': 'success',
            'data': {
                'success': audit_passed,
                'auditId': contract_audit.id,
                'auditDetails': {
                    'securityChecks': high_severity_issues
                } if high_severity_issues else None
            }
        })

    except Exception as e:
        logger.error(f"Error in submit_audit: {str(e)}")
        return jsonify({
            'code': 500,
            'message': str(e),
            'data': {'success': False}
        }), 500

@bp.route('/register/<int:audit_id>', methods=['POST'])
def register_contract(audit_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({'code': 400, 'message': 'No input data provided'}), 400

        # 获取审核记录
        audit = ContractAudit.query.get_or_404(audit_id)
        
        # 检查审核状态
        if audit.audit_status != 1:
            return jsonify({'code': 400, 'message': '只有审核通过的合约才能注册'}), 400
        
        # 检查合约地址是否已在 contracts 表中存在
        existing_contract = Contract.query.filter_by(address=data['address']).first()
        if existing_contract:
            # 如果合约已存在，只更新审核记录的关联信息
            audit.contract_address = data['address']
            audit.tx_hash = data['tx_hash']
            audit.register_time = datetime.utcnow()
            audit.registered_contract_id = existing_contract.id
            
            try:
                db.session.commit()
                return jsonify({
                    'code': 200,
                    'message': 'success',
                    'data': {
                        'contractId': existing_contract.id
                    }
                })
            except Exception as e:
                db.session.rollback()
                logger.error(f"Error updating audit record: {str(e)}")
                return jsonify({
                    'code': 500,
                    'message': '更新审核记录失败'
                }), 500
        
        # 如果合约地址不存在，创建新的合约记录
        contract = Contract(
            name=audit.name,
            address=data['address'],
            source_code=audit.source_code,
            status=1,
            create_time=datetime.utcnow()
        )
        
        try:
            # 修改这部分，使用原生SQL插入
            result = db.session.execute(
                """
                INSERT INTO contracts (name, address, source_code, create_time, status)
                VALUES (:name, :address, :source_code, :create_time, :status)
                RETURNING id
                """,
                {
                    'name': contract.name,
                    'address': contract.address,
                    'source_code': contract.source_code,
                    'create_time': contract.create_time,
                    'status': contract.status
                }
            )
            new_contract_id = result.scalar()
            
            # 更新审核记录的注册信息
            audit.contract_address = data['address']
            audit.tx_hash = data['tx_hash']
            audit.register_time = datetime.utcnow()
            audit.registered_contract_id = new_contract_id
            
            db.session.commit()
            
            return jsonify({
                'code': 200,
                'message': 'success',
                'data': {
                    'contractId': new_contract_id
                }
            })
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Database error during contract registration: {str(e)}")
            return jsonify({
                'code': 500,
                'message': '数据库操作失败'
            }), 500
            
    except Exception as e:
        logger.error(f"Error registering contract: {str(e)}")
        return jsonify({
            'code': 500,
            'message': str(e)
        }), 500

@bp.route('/list', methods=['GET'])
def get_audit_list():
    try:
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('pageSize', 10, type=int)
        
        query_obj = ContractAudit.query.order_by(ContractAudit.submit_time.desc())
        
        # 分页
        pagination = query_obj.paginate(
            page=page, per_page=page_size, error_out=False
        )

        audit_list = [{
            'id': item.id,
            'name': item.name,
            'submit_time': item.submit_time.isoformat(),
            'audit_status': item.audit_status,
            'audit_result': item.audit_result
        } for item in pagination.items]

        return jsonify({
            'code': 200,
            'message': 'success',
            'data': {
                'list': audit_list,
                'total': pagination.total
            }
        })
    except Exception as e:
        logger.error(f"Error getting audit list: {str(e)}")
        return jsonify({
            'code': 500,
            'message': 'Internal server error'
        }), 500

@bp.route('/registered', methods=['GET'])
def get_registered_contracts():
    try:
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('pageSize', 10, type=int)
        
        # 查询已注册的合约审核记录
        query = ContractAudit.query.filter(
            ContractAudit.contract_address.isnot(None)
        ).order_by(ContractAudit.register_time.desc())
        
        pagination = query.paginate(
            page=page, per_page=page_size, error_out=False
        )
        
        contracts = [{
            'id': item.id,
            'name': item.name,
            'address': item.contract_address,
            'tx_hash': item.tx_hash,
            'register_time': item.register_time.isoformat() if item.register_time else None
        } for item in pagination.items]
        
        return jsonify({
            'code': 200,
            'message': 'success',
            'data': {
                'list': contracts,
                'total': pagination.total
            }
        })
        
    except Exception as e:
        logger.error(f"Error getting registered contracts: {str(e)}")
        return jsonify({
            'code': 500,
            'message': str(e)
        }), 500

@bp.route('/detail/<int:audit_id>', methods=['GET'])
def get_audit_detail(audit_id):
    try:
        # 获取审核记录
        audit = ContractAudit.query.get_or_404(audit_id)
        
        return jsonify({
            'code': 200,
            'message': 'success',
            'data': {
                'id': audit.id,
                'name': audit.name,
                'submit_time': audit.submit_time.isoformat(),
                'audit_status': audit.audit_status,
                'audit_result': audit.audit_result
            }
        })
    except Exception as e:
        logger.error(f"Error getting audit detail: {str(e)}")
        return jsonify({
            'code': 500,
            'message': 'Internal server error'
        }), 500
