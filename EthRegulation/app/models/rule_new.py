from datetime import datetime
from app.extensions import db

class RuleNew(db.Model):
    __tablename__ = 'rules_new'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    contract_address = db.Column(db.String(42), nullable=False)
    description = db.Column(db.Text)
    owner = db.Column(db.String(255), nullable=False)
    functions = db.Column(db.JSON)  # 使用JSON类型存储函数和参数
    status = db.Column(db.Integer, default=0)  # 0: 待审核, 1: 已上线, 2: 已下线
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    rule_number = db.Column(db.String(20))
    regulator_address = db.Column(db.String(42)) 