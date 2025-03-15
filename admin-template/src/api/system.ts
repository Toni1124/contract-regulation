// 模拟系统配置数据
const mockSystemConfig = {
  regions: [
    { id: 1, name: "香港" },
    { id: 2, name: "中国大陆" },
    { id: 3, name: "不限" },
    { id: 4, name: "澳门" },
    { id: 5, name: "深圳" }
  ],
  operators: [
    { id: 1, name: "Admin" },
    { id: 2, name: "Operator" },
    { id: 3, name: "Manager" },
    { id: 4, name: "Auditor" }
  ],
  organizations: [
    { id: 1, name: "机构A" },
    { id: 2, name: "机构B" },
    { id: 3, name: "机构C" },
    { id: 4, name: "机构D" }
  ]
}

import request from '@/utils/request'

// 获取系统配置
export const getSystemConfig = () => {
  // 使用真实API
  return request({
    url: 'http://127.0.0.1:5000/api/system/config',
    method: 'get'
  })

  /* // 使用mock数据
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        code: 200,
        message: 'success',
        data: mockSystemConfig
      })
    }, 100) // 模拟网络延迟
  })
  */
}

/* 
// 真实 API 调用（后续接入后端时使用）
import request from '@/utils/request'

export const getSystemConfig = () => {
  return request({
    url: '/api/system/config',
    method: 'get'
  })
}
*/ 