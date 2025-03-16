import request from '@/utils/request'
import { BASE_URL } from './config'

// 格式化日期时间
const formatDateTime = (date: Date): string => {
  return date.toISOString().slice(0, 19).replace('T', ' ')  // 格式：'YYYY-MM-DD HH:mm:ss'
}

// 生成模拟数据
const generateMockData = () => {
  const organizations = ['中国人民银行', '中央网信办', '香港金管局']
  const regions = ['香港', '中国大陆', '不限', '澳门', '深圳']
  const operators = ['Admin', 'Operator']
  
  // 生成数据数组
  const data = Array.from({ length: 100 }, (_, index) => {
    // 从当前时间开始，每条记录间隔递减1小时
    const date = new Date(Date.now() - index * 60 * 60 * 1000)
    
    return {
      id: index + 1,
      address: `0x742d35Cc6634C0532925a3b844Bc454e4438f${index.toString(16).padStart(2, '0')}e`,
      operateTime: formatDateTime(date), // 使用递减的时间
      operator: operators[Math.floor(Math.random() * operators.length)],
      type: Math.random() > 0.5 ? 1 : 2,
      organization: organizations[Math.floor(Math.random() * organizations.length)],
      region: regions[Math.floor(Math.random() * regions.length)]
    }
  })

  // 确保数据按时间降序排序
  return data.sort((a, b) => 
    new Date(b.operateTime).getTime() - new Date(a.operateTime).getTime()
  )
}

// 模拟后端数据
let mockData = generateMockData()

// 定义接口返回数据类型
interface BlackWhiteListItem {
  id: number
  address: string
  operateTime: string  // 确保与后端返回的字段名匹配
  operator: string
  type: number        // 1: 白名单, 2: 黑名单
  organization: string
  region: string
}

interface ListResponse {
  code: number
  message: string
  data: {
    list: BlackWhiteListItem[]
    total: number
    page: number
    pageSize: number
  }
}

interface ErrorResponse {
  code: number
  message: string
  errors?: {
    [key: string]: string[]
  }
}

/**
 * 后端 API 文档
 * 
 * 1. 获取黑白名单列表
 * GET /api/black-white-list
 * 
 * 请求参数：
 * @param {number} page - 页码，从1开始
 * @param {number} pageSize - 每页条数
 * @param {string} [keyword] - 搜索关键词（可选，用于地址搜索）
 * @param {number} [type] - 类型筛选（可选，1-白名单，2-黑名单）
 * @param {string} [region] - 区域筛选（可选）
 * @param {string} [organization] - 机构筛选（可选）
 * @param {string} [operator] - 操作人筛选（可选）
 * 
 * 响应数据：
 * {
 *   code: 200,
 *   message: "success",
 *   data: {
 *     list: Array<{
 *       id: number,
 *       address: string,
 *       operateTime: string,  // 格式：YYYY-MM-DD HH:mm:ss
 *       operator: string,
 *       type: number,
 *       organization: string,
 *       region: string
 *     }>,
 *     total: number,
 *     page: number,
 *     pageSize: number
 *   }
 * }
 * 
 * 2. 添加黑白名单
 * POST /api/black-white-list
 * 
 * 请求体：
 * {
 *   address: string,
 *   operator: string,
 *   type: number,
 *   organization: string,
 *   region: string
 * }
 * 
 * 3. 更新黑白名单
 * PUT /api/black-white-list/{id}
 * 
 * 请求体：
 * {
 *   address: string,
 *   operator: string,
 *   type: number,
 *   organization: string,
 *   region: string
 * }
 * 
 * 4. 删除黑白名单
 * DELETE /api/black-white-list/{id}
 */

// 获取列表参数接口
interface ListParams {
  page: number
  pageSize: number
  keyword?: string
  type?: number
  region?: string
  organization?: string
  operator?: string
}

// 获取列表
export const getList = (params: ListParams) => {
  return request<ListResponse>({
    url: '/api/black-white-list',
    method: 'get',
    params
  })
}

// 添加
export const addItem = (data: {
  address: string
  operator: string
  type: number
  organization: string
  region: string
}) => {
  return request<BlackWhiteListItem | ErrorResponse>({
    url: '/api/black-white-list',
    method: 'post',
    data
  })
}

// 更新请求数据类型
interface UpdateItemData {
  address: string
  operator: string
  type: number
  organization: string
  region: string
}

// 更新
export const updateItem = (id: number, data: UpdateItemData) => {
  if (typeof id !== 'number') {
    throw new Error('Invalid ID');
  }
  
  return request<BlackWhiteListItem | ErrorResponse>({
    url: `/api/black-white-list/${id}`,
    method: 'put',
    data
  })
}

// 删除
export const deleteItem = (id: number) => {
  return request<null>({
    url: `/api/black-white-list/${id}`,
    method: 'delete'
  })
}