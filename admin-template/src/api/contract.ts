import request from '@/utils/request'
import { BASE_URL } from './config'

// 合约信息接口
export interface ContractItem {
  id: number
  address: string
  txHash: string
  name: string
  description: string
  sourceCode: string
  version: string
  optimization: boolean
  status: number // 0: 待审核, 1: 通过, 2: 拒绝
  submitTime: string
  comment?: string
  auditDetails?: {
    securityChecks: Array<{
      title: string
      severity: string
      description: string
      location?: {
        line: number
        code: string
      }
    }>
    regulations?: Array<{
      title: string
      content: string
      violation: string
    }>
    codeQuality: Array<{
      type: string
      title: string
      suggestion: string
    }>
    gasOptimization: Array<{
      title: string
      description: string
      example?: {
        before: string
        after: string
      }
    }>
  }
}

// 获取合约列表
export const getContractList = async (params: {
  page: number
  pageSize: number
  query?: string
  status?: number | string
}) => {
  // 模拟数据
  const allData = [
    {
      id: 1,
      address: '0xf3a1c121fe0a209fcac956831fa7a91c52e76542',
      txHash: '0x9876543210987654321098765432109876543210',
      name: 'GameToken',
      description: '游戏代币合约',
      sourceCode: 'contract GameToken is ERC20 { ... }',
      version: '0.8.17',
      optimization: true,
      status: 2, // 审核失败
      submitTime: '2024-02-24 14:24:34',
      comment: '违反监管合规要求',
      auditDetails: {
        securityChecks: [
          {
            title: '监管合规性问题',
            severity: 'error',
            description: '该合约功能涉嫌违反《关于进一步防范和整治虚拟货币交易炒作活动的通知》（网信办发〔2021〕84号）第三条规定：\n\n1. 合约包含概率性游戏功能，可用于在线博彩\n2. 智能合约中发现可疑的奖励分配机制，存在赌博特征\n3. 缺乏必要的用户身份认证和资格审查机制',
            location: {
              line: 42,
              code: 'function playGame(uint256 betAmount) public returns (uint256 reward) {\n    require(betAmount > 0, "Bet amount must be positive");\n    uint256 randomNumber = uint256(keccak256(abi.encodePacked(block.timestamp)));\n    reward = (randomNumber % 100 > 50) ? betAmount * 2 : 0;\n    // ...\n}'
            }
          }
        ],
        regulations: [
          {
            title: '《关于进一步防范和整治虚拟货币交易炒作活动的通知》（网信办发〔2021〕84号）',
            content: '第三条：严禁利用虚拟货币进行非法金融活动。金融机构、非银行支付机构和互联网企业不得为虚拟货币相关业务活动提供服务。严禁利用虚拟货币从事非法金融活动，严防虚拟货币交易炒作风险。',
            violation: '合约中包含概率性游戏功能和奖励分配机制，可被用于赌博活动，违反了该条例关于防范虚拟货币非法金融活动的规定。'
          },
          {
            title: '《关于防范以"虚拟货币"名义进行非法集资的风险提示》（银保监会）',
            content: '各类以"虚拟货币"名义进行的集资、传销等非法金融活动具有较大风险，消费者应当提高风险意识。',
            violation: '合约中的奖励机制可能被用于非法集资活动，且缺乏必要的用户身份认证机制。'
          }
        ],
        codeQuality: [],
        gasOptimization: []
      }
    },
    {
      id: 2,
      address: '0x218a810d0b8e2b81c6a7a3302b8ac76d89182d45',
      txHash: '0x8765432109876543210987654321098765432109',
      name: 'StableCoin',
      description: '稳定币合约',
      sourceCode: 'contract StableCoin { ... }',
      version: '0.8.20',
      optimization: true,
      status: 0, // 审核中
      submitTime: '2024-02-22 16:54:33',
      comment: '审核中'
    },
    {
      id: 3,
      address: '0x150bCF49Ee8E2Bd9f59e991821D4a1c52e76542',
      txHash: '0x7654321098765432109876543210987654321098',
      name: 'VotingSystem',
      description: '投票系统合约',
      version: '0.8.17',
      optimization: false,
      status: 2, // 审核失败
      submitTime: '2024-02-22 16:47:20',
      comment: '存在安全漏洞',
      auditDetails: {
        securityChecks: [
          {
            title: '重入攻击风险',
            severity: 'error',
            description: '投票合约中发现重入攻击风险，攻击者可能重复投票',
            location: {
              line: 156,
              code: 'function vote(uint256 proposalId) public {\n    require(!hasVoted[msg.sender][proposalId]);\n    (bool success, ) = msg.sender.call("");\n    hasVoted[msg.sender][proposalId] = true;\n}'
            }
          }
        ],
        codeQuality: [
          {
            type: 'warning',
            title: '状态变量保护',
            suggestion: '建议在状态变量更新前进行所有外部调用'
          }
        ],
        gasOptimization: []
      }
    },
    {
      id: 4,
      address: '0x389bCF49Ee8E2Bd9f59e991821D4a1c52e76123',
      txHash: '0x7654321098765432109876543210987654321567',
      name: 'SupplyChain',
      description: '供应链溯源合约',
      version: '0.8.17',
      optimization: true,
      status: 1, // 审核通过
      submitTime: '2024-02-22 15:30:20',
      comment: '合约安全性良好，满足业务需求',
      auditDetails: {
        securityChecks: [],
        codeQuality: [
          {
            type: 'success',
            title: '代码结构',
            suggestion: '代码结构清晰，安全性检查完善'
          }
        ],
        gasOptimization: [
          {
            title: '存储优化建议',
            description: '建议使用结构体打包存储相关数据，可以节省gas',
            example: {
              before: 'mapping(uint256 => string) public productName;\nmapping(uint256 => string) public manufacturer;',
              after: 'struct Product {\n    string name;\n    string manufacturer;\n}\nmapping(uint256 => Product) public products;'
            }
          }
        ]
      }
    }
  ]

  // 根据查询条件过滤数据
  let filteredData = allData.filter(item => {
    // 状态筛选
    if (params.status !== undefined && params.status !== '') {
      if (item.status !== Number(params.status)) return false
    }
    
    // 地址或名称搜索（前缀匹配）
    if (params.query) {
      const query = params.query.toLowerCase()
      return item.address.toLowerCase().startsWith(query) || 
             item.name.toLowerCase().startsWith(query)
    }
    
    return true
  })

  // 分页
  const start = (params.page - 1) * params.pageSize
  const end = start + params.pageSize
  const pageData = filteredData.slice(start, end)

  // 返回结果
  return Promise.resolve([null, {
    code: 200,
    data: {
      list: pageData,
      total: filteredData.length
    }
  }])
}

// 提交合约审核
export const submitContract = async (data: Omit<ContractItem, 'id' | 'status' | 'submitTime'>) => {
  // 直接返回成功
  return Promise.resolve([null, {
    code: 200,
    data: {
      ...data,
      id: Math.floor(Math.random() * 1000),
      status: 1,
      submitTime: new Date().toISOString()
    },
    message: 'success'
  }])
}

// 验证合约代码
export const verifyContractCode = async (data: {
  address: string
  sourceCode: string
  version: string
  optimization: boolean
}) => {
  // 直接返回验证成功
  return Promise.resolve({
    success: true,
    message: '合约验证成功',
    data: {
      bytecodeMatch: true,
      abiMatch: true
    }
  })
}

// 获取交易信息
export const getTransactionInfo = async (txHash: string) => {
  // 返回模拟数据
  return Promise.resolve({
    code: 200,
    data: {
      txHash,
      contractAddress: '0x1234567890123456789012345678901234567890',
      from: '0x0987654321098765432109876543210987654321',
      blockNumber: 12345678,
      timestamp: new Date().toISOString()
    }
  })
}

// 合约相关的API接口定义 