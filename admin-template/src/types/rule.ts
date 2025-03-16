interface RuleParameter {
  id?: number
  name: string
  type: string
  condition: string
  value: string
}

interface RuleFunction {
  id?: number
  name: string
  params: RuleParameter[]
}

interface Rule {
  id?: number
  name: string
  contractAddress: string
  description: string
  owner: string
  functions: RuleFunction[]
}

// 用于提交的数据接口
interface RuleSubmitData {
  name: string
  contractAddress: string
  description: string
  owner: string
  functions: Array<{
    id?: number
    name: string
    params: Array<{
      id?: number
      name: string
      type: string
      condition: string
      value: string
    }>
  }>
} 