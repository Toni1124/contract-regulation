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
        
        # 检查审核是否通过
        if audit.audit_status != 1:
            return jsonify({
                'code': 400,
                'message': 'Contract audit not passed'
            }), 400

        # 创建新的合约记录
        contract = Contract(
            name=audit.name,
            address=data['address'],
            source_code=audit.source_code,
            status=1  # 已部署
        )
        
        db.session.add(contract)
        
        # 更新审核记录关联的已注册合约ID
        audit.registered_contract_id = contract.id
        
        db.session.commit()

        return jsonify({
            'code': 200,
            'message': 'Contract registered successfully',
            'data': {
                'contractId': contract.id
            }
        })

    except Exception as e:
        logger.error(f"Error in register_contract: {str(e)}")
        db.session.rollback()
        return jsonify({
            'code': 500,
            'message': str(e)
        }), 500
