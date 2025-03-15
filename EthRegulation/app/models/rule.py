from datetime import datetime
from app.extensions import db
from typing import List

class Rule(db.Model):
    __tablename__ = 'rules'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    regulator_address = db.Column(db.String(42), nullable=False)
    description = db.Column(db.Text)
    contract_address = db.Column(db.String(42), nullable=False)
    owner = db.Column(db.String(100), nullable=False)
    rule_id = db.Column(db.String(20), unique=True, nullable=False)
    status = db.Column(db.Integer, default=0)  # 0: 待审核, 1: 已上线, 2: 已下线
    create_time = db.Column(db.DateTime, default=datetime.now)
    functions = db.relationship('RuleFunction', backref='rule', lazy=True, cascade='all, delete-orphan')

class RuleFunction(db.Model):
    __tablename__ = 'rule_functions'
    
    id = db.Column(db.Integer, primary_key=True)
    rule_id = db.Column(db.Integer, db.ForeignKey('rules.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    params = db.relationship('RuleParameter', backref='function', lazy=True, cascade='all, delete-orphan')

class RuleParameter(db.Model):
    __tablename__ = 'rule_parameters'
    
    id = db.Column(db.Integer, primary_key=True)
    function_id = db.Column(db.Integer, db.ForeignKey('rule_functions.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    condition = db.Column(db.String(20), nullable=False)
    value = db.Column(db.String(255), nullable=False) 