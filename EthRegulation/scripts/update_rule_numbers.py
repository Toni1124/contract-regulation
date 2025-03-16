from app import create_app
from app.models.rule_new import RuleNew
from app.extensions import db
from datetime import datetime
import random

def get_contract_suffix(address):
    # 获取合约地址的后4位
    if address and len(address) >= 4:
        return address[-4:]
    return 'XXXX'

def update_rule_numbers():
    app = create_app()
    with app.app_context():
        try:
            # 获取所有规则，按创建时间排序
            rules = RuleNew.query.order_by(RuleNew.create_time).all()
            
            # 用于跟踪每天的序号
            date_counters = {}
            
            for rule in rules:
                # 直接使用 create_time，因为它已经是 datetime 对象
                create_time = rule.create_time
                year = create_time.strftime('%y')
                date_key = create_time.strftime('%Y%m%d')
                timestamp = create_time.strftime('%H%M')
                
                # 获取合约地址后4位
                contract_suffix = get_contract_suffix(rule.contract_address)
                
                # 获取当天的序号
                if date_key not in date_counters:
                    date_counters[date_key] = 1
                else:
                    date_counters[date_key] += 1
                
                sequence = str(date_counters[date_key]).zfill(3)  # 序号补零到3位
                
                # 生成新的规则编号: R-年份-合约后4位-时间戳-序号
                new_rule_number = f"R-{year}-{contract_suffix}-{timestamp}-{sequence}"
                
                # 更新规则编号
                rule.rule_number = new_rule_number
                print(f"Updating rule {rule.id}: {new_rule_number}")
            
            # 提交所有更改
            db.session.commit()
            print("Successfully updated all rule numbers")
            
        except Exception as e:
            db.session.rollback()
            print(f"Error updating rule numbers: {str(e)}")

if __name__ == '__main__':
    update_rule_numbers() 