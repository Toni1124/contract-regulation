from datetime import datetime
from app import db
from app.constants.enums import ListType, Region, Organization, Operator
from typing import Any

class BlackWhiteList(db.Model):
    __tablename__ = 'black_white_list'
    
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(42), unique=True, nullable=False)  # 以太坊地址长度为42（包含0x前缀）
    operate_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    operator = db.Column(db.String(50), nullable=False)
    type = db.Column(db.Integer, nullable=False)  # 1: 白名单, 2: 黑名单
    organization = db.Column(db.String(100), nullable=False)
    region = db.Column(db.String(50), nullable=False)

    def __repr__(self) -> str:
        return f'<BlackWhiteList {self.address}>'

    @property
    def list_type(self) -> ListType:
        return ListType(self.type)

    @property
    def region_enum(self) -> Region:
        return Region(self.region)

    @property
    def operator_enum(self) -> Operator:
        return Operator(self.operator)

    @property
    def organization_enum(self) -> Organization:
        return Organization(self.organization) 