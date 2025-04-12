import request from '@/utils/request'

// 审核结果接口定义
export interface SecurityCheck {
  title: string
  severity: string
  description: string
  check: string
  confidence: string
  location?: {
    line: number
    code: string
  }
}

export interface AuditResponse {
  code: number
  message: string
  data: {
    success: boolean
    auditId?: number
    error?: string
    auditDetails?: Array<{
      title: string
      severity: string
      description: string
      check: string
      confidence: string
      location?: {
        line: number
        code: string
      }
    }>
  }
}

// 审核记录接口
export interface ContractAuditItem {
  id: number
  name: string
  submit_time: string
  audit_status: number
  audit_result?: {
    securityChecks: SecurityCheck[]
  }
}

// 注册记录接口
export interface RegisteredContract {
  id: number
  name: string
  address: string
  tx_hash: string
  register_time: string
}

// 提交合约审核
export const submitContractAudit = (data: {
  name: string
  source_code: string
  version: string
}) => {
  return request<AuditResponse>({
    url: '/api/contract-audit/submit',
    method: 'post',
    data
  })
}

// 注册已审核通过的合约
export const registerContract = (auditId: number, data: {
  address: string
  tx_hash: string
}) => {
  return request<{
    code: number
    message: string
    data: {
      contractId: number
    }
  }>({
    url: `/api/contract-audit/register/${auditId}`,
    method: 'post',
    data
  })
}

// 获取审核列表
export const getAuditList = (params: {
  page: number
  pageSize: number
  query?: string
  status?: number
}) => {
  return request<{
    code: number
    message: string
    data: {
      list: ContractAuditItem[]
      total: number
    }
  }>({
    url: '/api/contract-audit/list',
    method: 'get',
    params
  })
}

// 获取注册记录列表
export const getRegisteredContracts = (params: {
  page: number
  pageSize: number
}) => {
  return request<{
    code: number
    message: string
    data: {
      list: RegisteredContract[]
      total: number
    }
  }>({
    url: '/api/contract-audit/registered',
    method: 'get',
    params
  })
}

// 获取审核详情
export const getAuditDetail = (id: number) => {
  return request<{
    code: number
    message: string
    data: {
      id: number
      name: string
      submit_time: string
      audit_status: number
      audit_result: {
        securityChecks: SecurityCheck[]
      } | null
    }
  }>({
    url: `/api/contract-audit/detail/${id}`,
    method: 'get'
  })
}

// 获取已注册合约详情
export const getRegisteredContractDetail = (id: number) => {
  return request<{
    code: number
    message: string
    data: {
      id: number
      name: string
      address: string
      tx_hash: string
      register_time: string
      source_code: string
      audit_result: {
        securityChecks: SecurityCheck[]
      }
    }
  }>({
    url: `/api/contract-audit/registered-detail/${id}`,
    method: 'get'
  })
}
