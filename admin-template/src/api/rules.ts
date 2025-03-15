import request from './request'

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
  // Mock data
  const mockData = {
    code: 200,
    message: 'success',
    data: {
      list: [
        {
          id: 1,
          name: '资金流向监控规则',
          regulatorAddress: '0x1234567890abcdef1234567890abcdef12345678',
          description: '监控资金流向，防止洗钱行为',
          contractAddress: '0xabcdef1234567890abcdef1234567890abcdef12',
          owner: 'super',
          ruleId: 'RULE20240306001',
          status: 1,
          createTime: '2024-03-06 14:30:00'
        }
      ],
      total: 1
    }
  }

  return Promise.resolve(mockData)
  // return request({
  //   url: '/rules',
  //   method: 'get',
  //   params
  // })
}

/**
 * @api {post} /api/rules 添加监管规则
 * @apiName AddRule
 * @apiGroup Rules
 * @apiParam {String} name 规则名称
 * @apiParam {String} contractAddress 合约地址
 * @apiParam {String} [description] 规则描述
 * @apiParam {String} owner 所属用户
 * @apiParam {String} functionName 函数名称
 * @apiParam {Object[]} parameters 函数参数列表
 * @apiParam {File} [file] 规则文件
 */
export const addRule = (data: FormData) => {
  // Mock response
  return Promise.resolve({
    code: 200,
    message: 'success',
    data: {
      id: 2,
      name: data.get('name'),
      regulatorAddress: '0x1234567890abcdef1234567890abcdef12345678',
      description: data.get('description'),
      contractAddress: data.get('contractAddress'),
      owner: data.get('owner'),
      ruleId: 'RULE20240306002',
      status: 0,
      createTime: new Date().toISOString()
    }
  })
  // return request({
  //   url: '/rules',
  //   method: 'post',
  //   data,
  //   headers: {
  //     'Content-Type': 'multipart/form-data'
  //   }
  // })
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
export const updateRule = (id: number, data: FormData) => {
  // Mock response
  return Promise.resolve({
    code: 200,
    message: 'success'
  })
  // return request({
  //   url: `/rules/${id}`,
  //   method: 'put',
  //   data,
  //   headers: {
  //     'Content-Type': 'multipart/form-data'
  //   }
  // })
}

/**
 * @api {delete} /api/rules/:id 删除监管规则
 * @apiName DeleteRule
 * @apiGroup Rules
 * @apiParam {Number} id 规则ID
 */
export const deleteRule = (id: number) => {
  // Mock response
  return Promise.resolve({
    code: 200,
    message: 'success'
  })
  // return request({
  //   url: `/rules/${id}`,
  //   method: 'delete'
  // })
}

/**
 * @api {get} /api/contracts 获取已部署合约列表
 * @apiName GetContractList
 * @apiGroup Contracts
 * @apiParam {String} [keyword] 搜索关键词
 */
export const getContractList = (params?: { keyword?: string }) => {
  // Mock response
  return Promise.resolve({
    code: 200,
    message: 'success',
    data: {
      list: [
        {
          id: 1,
          name: 'TokenContract',
          address: '0x1234567890abcdef1234567890abcdef12345678',
          sourceCode: `
contract TokenContract {
    uint256 public totalSupply;
    
    function store(uint256 num) public {
        totalSupply = num;
    }
}
          `
        }
      ]
    }
  })
  // return request({
  //   url: '/contracts',
  //   method: 'get',
  //   params
  // })
} 