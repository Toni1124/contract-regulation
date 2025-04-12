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

export interface ContractAuditItem {
  id: number
  name: string
  source_code: string
  version: string
  submit_time: string
  audit_status: number // 0: 待审核, 1: 通过, 2: 未通过
  audit_result?: {
    securityChecks: SecurityCheck[]
  }
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
