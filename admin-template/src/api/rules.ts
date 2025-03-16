import request from '@/utils/request'
import { BASE_URL } from './config'

/**
 * @api {get} /api/rules 获取监管规则列表
 * @apiName GetRuleList
 * @apiGroup Rules
 * @apiParam {Number} page 页码
 * @apiParam {Number} pageSize 每页数量
 * @apiParam {String} [keyword] 搜索关键词
 * @apiSuccess {Object[]} list 规则列表
 * @apiSuccess {Number} total 总数
 */
export const getRuleList = (params: {
  page: number
  pageSize: number
  keyword?: string
}) => {
  return request({
    url: `${BASE_URL}/rules`,
    method: 'get',
    params
  })
}

interface RuleResponse {
  code: number
  message: string
  data: {
    list?: any[]
    total?: number
  }
}

interface RuleData {
  name: string
  contractAddress: string
  description: string
  owner: string
  functions: Array<{
    name: string
    params: Array<{
      name: string
      type: string
      condition: string
      value: string
    }>
  }>
}

/**
 * @api {post} /api/rules 添加监管规则
 * @apiName AddRule
 * @apiGroup Rules
 */
export const addRule = (data: RuleData) => {
  return request<RuleResponse>({
    url: `${BASE_URL}/api/rules`,
    method: 'post',
    data,
    headers: {
      'Content-Type': 'application/json'
    }
  })
}

/**
 * @api {put} /api/rules/:id 更新监管规则
 * @apiName UpdateRule
 * @apiGroup Rules
 * @apiParam {Number} id 规则ID
 * @apiParam {String} [name] 规则名称
 * @apiParam {String} [contractAddress] 合约地址
 * @apiParam {String} [description] 规则描述
 * @apiParam {String} [functionName] 函数名称
 * @apiParam {Object[]} [parameters] 函数参数列表
 * @apiParam {File} [file] 规则文件
 */
export const updateRule = (id: number, data: any) => {
  return request({
    url: `${BASE_URL}/api/rules/${id}`,
    method: 'put',
    data,
    headers: {
      'Content-Type': 'application/json'
    }
  })
}

/**
 * @api {delete} /api/rules/:id 删除监管规则
 * @apiName DeleteRule
 * @apiGroup Rules
 * @apiParam {Number} id 规则ID
 */
export const deleteRule = (id: number) => {
  return request({
    url: `${BASE_URL}/api/rules/${id}`,
    method: 'delete'
  })
}

interface ContractResponse {
  code: number
  message: string
  data: {
    list: Array<{
      id: number
      name: string
      address: string
      source_code: string
      abi: any
      create_time: string
      status: number
    }>
    total: number
  }
}

/**
 * @api {get} /api/contracts 获取已部署合约列表
 * @apiName GetContractList
 * @apiGroup Contracts
 * @apiParam {String} [keyword] 搜索关键词
 */
export const getContractList = (params?: { keyword?: string }) => {
  return request<ContractResponse>({
    url: '/api/contracts',
    method: 'get',
    params
  })
} 