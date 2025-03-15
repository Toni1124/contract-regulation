from app import create_app
from app.extensions import db
from app.models.black_white_list import BlackWhiteList
from datetime import datetime, timedelta
import random

def generate_eth_address():
    # 生成随机的ETH地址
    return '0x' + ''.join(random.choices('0123456789abcdef', k=40))

def generate_test_data():
    app = create_app()
    with app.app_context():
        # 清空现有数据（可选）
        # BlackWhiteList.query.delete()
        
        operators = ['Admin', 'Operator']
        types = [1, 2]  # 1: 白名单, 2: 黑名单
        organizations = ['中国人民银行', '中央网信办', '香港金管局']
        regions = ['香港', '中国大陆', '不限', '澳门', '深圳']
        
        # 生成100条测试数据
        for i in range(100):
            # 随机生成操作时间（最近30天内）
            random_days = random.randint(0, 30)
            operate_time = datetime.now() - timedelta(days=random_days)
            
            item = BlackWhiteList(
                address=generate_eth_address(),
                operate_time=operate_time,
                operator=random.choice(operators),
                type=random.choice(types),
                organization=random.choice(organizations),
                region=random.choice(regions)
            )
            db.session.add(item)
        
        try:
            db.session.commit()
            print("Successfully generated 100 test records!")
        except Exception as e:
            db.session.rollback()
            print(f"Error occurred: {str(e)}")

if __name__ == '__main__':
    generate_test_data() 