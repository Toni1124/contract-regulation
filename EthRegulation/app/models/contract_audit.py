from datetime import datetime
from app.extensions import db

class ContractAudit(db.Model):
    __tablename__ = 'contract_audits'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, comment='合约名称')
    source_code = db.Column(db.Text, nullable=False, comment='合约源代码')
    version = db.Column(db.String(20), nullable=False, comment='Solidity版本')
    submit_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, comment='提交时间')
    audit_status = db.Column(db.Integer, nullable=False, default=0, comment='审核状态：0-待审核，1-通过，2-未通过')
    audit_result = db.Column(db.JSON, nullable=True, comment='Slither分析结果')
    
    # 注册相关信息
    contract_address = db.Column(db.String(42), nullable=True, comment='已部署的合约地址')
    tx_hash = db.Column(db.String(66), nullable=True, comment='部署交易哈希')
    register_time = db.Column(db.DateTime, nullable=True, comment='注册时间')
    
    # 关联到contracts表
    registered_contract_id = db.Column(db.Integer, db.ForeignKey('contracts.id'), nullable=True)
    registered_contract = db.relationship('Contract', backref=db.backref('audit_record', uselist=False))

    def __repr__(self):
        return f'<ContractAudit {self.name}>'