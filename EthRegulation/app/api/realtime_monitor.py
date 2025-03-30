from flask import Blueprint, request, jsonify
import psycopg2
from datetime import datetime
import json
from typing import Dict, Any, Tuple
import decimal

bp = Blueprint('realtime_monitor', __name__, url_prefix='/api')

def get_db_connection():
    return psycopg2.connect(
        host='10.0.2.251',
        dbname='db',
        user='ethereum',
        password='emm20240809!'
    )

# 添加 JSON 编码器来处理特殊类型
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, bytes):
            return obj.decode('utf-8')
        return super().default(obj)

@bp.route('/realtime-monitor/initial', methods=['GET'])
def get_initial_data() -> Tuple[Dict[str, Any], int]:
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
        SELECT 
            block_number,
            block_timestamp,
            transaction_index,
            value,
            gas,
            gas_price,
            nonce,
            from_address,
            to_address,
            receipt_contract_address,
            receipt_root,
            block_hash,
            input,
            hash,
            function_signature,
            function_name,
            decoded_parameters,
            rules_check_passed,
            rules_check_message
        FROM eth_transaction_details 
        ORDER BY block_timestamp ASC, block_number ASC, transaction_index ASC
        LIMIT 1000
        """
        
        print("Executing initial query for oldest 1000 records")
        cursor.execute(query)
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        print(f"Found {len(rows)} rows")
        
        # 将查询结果转换为字典列表
        result = []
        for idx, row in enumerate(rows):
            try:
                item = {}
                for col, val in zip(columns, row):
                    # 特殊类型处理
                    if isinstance(val, decimal.Decimal):
                        item[col] = str(val)
                    elif isinstance(val, datetime):
                        item[col] = val.isoformat()
                    elif isinstance(val, bytes):
                        item[col] = val.decode('utf-8')
                    elif val is None:
                        item[col] = ''
                    else:
                        item[col] = val
                
                # decoded_parameters 处理
                if item['decoded_parameters']:
                    try:
                        if isinstance(item['decoded_parameters'], str):
                            item['decoded_parameters'] = json.loads(item['decoded_parameters'])
                        else:
                            item['decoded_parameters'] = dict(item['decoded_parameters'])
                    except Exception as e:
                        print(f"Error processing decoded_parameters for row {idx}: {e}")
                        item['decoded_parameters'] = str(item['decoded_parameters'])

                result.append(item)
                if idx % 100 == 0:
                    print(f"Processed {idx + 1} rows")
                    
            except Exception as e:
                print(f"Error processing row {idx}: {e}")
                print(f"Row data: {row}")
                continue
        
        print(f"Successfully processed all {len(result)} rows")
        
        # 使用 CustomJSONEncoder 进行序列化测试
        try:
            response_data = {
                'code': 200,
                'message': 'success',
                'data': result
            }
            json.dumps(response_data, cls=CustomJSONEncoder)
            return jsonify(response_data), 200
        except Exception as e:
            print(f"JSON serialization error: {str(e)}")
            # 返回简化的错误响应
            return {
                'code': 500,
                'message': f'JSON serialization error: {str(e)}'
            }, 500
        
    except Exception as e:
        import traceback
        print(f"Database error: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return {
            'code': 500,
            'message': str(e)
        }, 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@bp.route('/realtime-monitor/updates', methods=['GET'])
def get_updates():
    try:
        last_timestamp = request.args.get('last_timestamp')
        print(f"Received update request with timestamp: {last_timestamp}")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 修改查询逻辑，获取比当前时间戳更新的数据
        query = """
        SELECT 
            block_number,
            block_timestamp,
            transaction_index,
            value,
            gas,
            gas_price,
            nonce,
            from_address,
            to_address,
            receipt_contract_address,
            receipt_root,
            block_hash,
            input,
            hash,
            function_signature,
            function_name,
            decoded_parameters,
            rules_check_passed,
            rules_check_message
        FROM eth_transaction_details 
        WHERE block_timestamp > %s
        ORDER BY block_timestamp ASC, block_number ASC, transaction_index ASC
        LIMIT 3;
        """
        
        print(f"Executing query with timestamp: {last_timestamp}")
        cursor.execute(query, (last_timestamp,))
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        print(f"Found {len(rows)} new transactions since {last_timestamp}")
        
        result = []
        for idx, row in enumerate(rows):
            try:
                item = {}
                for col, val in zip(columns, row):
                    # 特殊类型处理
                    if isinstance(val, decimal.Decimal):
                        item[col] = str(val)
                    elif isinstance(val, datetime):
                        item[col] = val.isoformat()
                    elif isinstance(val, bytes):
                        item[col] = val.decode('utf-8')
                    elif val is None:
                        item[col] = ''
                    else:
                        item[col] = val
                
                # decoded_parameters 处理
                if item['decoded_parameters']:
                    try:
                        if isinstance(item['decoded_parameters'], str):
                            item['decoded_parameters'] = json.loads(item['decoded_parameters'])
                        else:
                            item['decoded_parameters'] = dict(item['decoded_parameters'])
                    except Exception as e:
                        print(f"Error processing decoded_parameters for row {idx}: {e}")
                        item['decoded_parameters'] = str(item['decoded_parameters'])

                result.append(item)
                
            except Exception as e:
                print(f"Error processing row {idx}: {e}")
                print(f"Row data: {row}")
                continue
        
        print(f"Successfully processed all {len(result)} rows")
        
        # 使用 CustomJSONEncoder 进行序列化
        response_data = {
            'code': 200,
            'message': 'success',
            'data': result
        }
        return jsonify(response_data), 200
        
    except Exception as e:
        print(f"Error in get_updates: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return jsonify({
            'code': 500,
            'message': str(e)
        }), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close() 