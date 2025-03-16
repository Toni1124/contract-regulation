from app import create_app, db
from app.models.black_white_list import BlackWhiteList
from datetime import datetime, timedelta
import random

def generate_mock_data():
    # 定义模拟数据
    organizations = ['中国人民银行', '中央网信办', '香港金管局']
    regions = ['香港', '中国大陆', '不限', '澳门', '深圳']
    operators = ['Admin', 'Operator']
    
    # 创建应用上下文
    app = create_app()
    
    with app.app_context():
        # 清空现有数据
        BlackWhiteList.query.delete()
        db.session.commit()
        
        # 生成100条记录
        for i in range(100):
            # 生成递减的时间
            current_time = datetime.utcnow() - timedelta(hours=i)
            
            # 生成以太坊地址
            address = f"0x742d35Cc6634C0532925a3b844Bc454e4438f{i:02x}e"
            
            # 创建记录
            record = BlackWhiteList(
                address=address,
                operate_time=current_time,
                operator=random.choice(operators),
                type=random.randint(1, 2),  # 1: 白名单, 2: 黑名单
                organization=random.choice(organizations),
                region=random.choice(regions)
            )
            
            db.session.add(record)
            
            # 每20条记录提交一次，以提高性能
            if (i + 1) % 20 == 0:
                try:
                    db.session.commit()
                    print(f"Committed records {i-18} to {i+1}")
                except Exception as e:
                    print(f"Error committing records: {str(e)}")
                    db.session.rollback()
        
        # 提交剩余记录
        try:
            db.session.commit()
            print("Successfully generated 100 records for black_white_list table")
        except Exception as e:
            print(f"Error in final commit: {str(e)}")
            db.session.rollback()

if __name__ == "__main__":
    generate_mock_data() 