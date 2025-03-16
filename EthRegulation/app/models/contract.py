from datetime import datetime
from app.extensions import db

class Contract(db.Model):
    __tablename__ = 'contracts'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(42), nullable=False, unique=True)
    source_code = db.Column(db.Text, nullable=False)
    abi = db.Column(db.JSON)
    create_time = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.Integer, default=1)  # 1: 已部署 