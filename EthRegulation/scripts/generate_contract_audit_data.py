from app import create_app, db
from app.models.contract_audit import ContractAudit
from datetime import datetime, timedelta
import random
import json

def generate_mock_data():
    app = create_app()
    
    with app.app_context():
        ContractAudit.query.delete()
        db.session.commit()
        
        sample_audit_results = [
            {
                "securityChecks": [{
                    "title": "重入攻击风险",
                    "severity": "High",
                    "description": "检测到可能存在重入攻击风险的代码模式",
                    "check": "reentrancy-eth",
                    "confidence": "High"
                }]
            },
            None  # 代表审核通过的情况
        ]

        for i in range(20):
            current_time = datetime.utcnow() - timedelta(hours=i)
            audit_status = random.choice([0, 1, 2])
            
            audit = ContractAudit(
                name=f"TestContract_{i}",
                source_code=f"contract TestContract_{i} {{ // Some code }}",
                version=random.choice(['0.8.0', '0.8.17', '0.8.20']),
                optimization=random.choice([True, False]),
                submit_time=current_time,
                audit_status=audit_status,
                audit_result=random.choice(sample_audit_results) if audit_status != 0 else None
            )
            
            db.session.add(audit)

        try:
            db.session.commit()
            print("Successfully generated 20 records for contract_audits table")
        except Exception as e:
            print(f"Error in commit: {str(e)}")
            db.session.rollback()

if __name__ == "__main__":
    generate_mock_data()
