import request from './request'
import axios from 'axios'

export interface TransactionData {
  block_number: number
  block_timestamp: string
  transaction_index: number
  value: string
  gas: number
  gas_price: number
  nonce: number
  from_address: string
  to_address: string
  receipt_contract_address: string
  receipt_root: string
  block_hash: string
  input: string
  hash: string
  function_signature: string
  function_name: string
  decoded_parameters: any
  rules_check_passed: boolean
  rules_check_message: string
}

export interface ApiResponse<T> {
  code: number
  message: string
  data: T
}

export async function getInitialData(): Promise<ApiResponse<TransactionData[]>> {
  try {
    const response = await request({
      url: '/api/realtime-monitor/initial',
      method: 'get',
      timeout: 60000
    });
    return response;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      if (error.code === 'ECONNABORTED') {
        throw new Error('请求超时，请稍后重试');
      }
      throw new Error(error.response?.data?.message || '获取数据失败');
    }
    throw error;
  }
}

export async function getUpdates(lastTimestamp: string): Promise<ApiResponse<TransactionData[]>> {
  try {
    const response = await request({
      url: '/api/realtime-monitor/updates',
      method: 'get',
      params: { last_timestamp: lastTimestamp },
      timeout: 30000  // 增加超时时间到30秒
    });
    return response;
  } catch (error) {
    console.error('Update request failed:', error);
    return {
      code: 200,
      message: 'success',
      data: []
    };
  }
} 