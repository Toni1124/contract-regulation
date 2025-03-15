# 监管规则管理系统 API 文档

## 目录
1. [规则管理接口](#规则管理接口)
2. [合约管理接口](#合约管理接口)

## 规则管理接口

### 1. 获取规则列表

**接口说明**: 获取监管规则列表，支持分页和关键词搜索  
**调用位置**: `src/views/RuleManagement/index.vue` 的 `fetchData` 方法  
**请求方法**: GET  
**请求路径**: `/api/rules`  

**请求参数**:
```typescript
{
  page: number      // 页码
  pageSize: number  // 每页数量
  keyword?: string  // 搜索关键词（可选）
}
```

**响应数据**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "list": [
      {
        "id": 1,
        "name": "资金流向监控规则",
        "regulatorAddress": "0x1234567890abcdef1234567890abcdef12345678",
        "description": "监控资金流向，防止洗钱行为",
        "contractAddress": "0xabcdef1234567890abcdef1234567890abcdef12",
        "owner": "super",
        "ruleId": "RULE20240306001",
        "status": 1,
        "createTime": "2024-03-06 14:30:00"
      }
    ],
    "total": 1
  }
}
```

### 2. 添加规则

**接口说明**: 新增监管规则  
**调用位置**: `src/views/RuleManagement/index.vue` 的 `handleSubmit` 方法（当 `dialogType === 'add'` 时）  
**请求方法**: POST  
**请求路径**: `/api/rules`  
**请求类型**: multipart/form-data  

**请求参数**:
```typescript
{
  name: string           // 规则名称
  contractAddress: string    // 合约地址
  description?: string  // 规则描述（可选）
  owner: string         // 所属用户
  functionName: string  // 函数名称
  parameters: string    // JSON字符串格式的参数列表
  file?: File          // 规则文件（可选）
}
```

**参数示例**:
```json
{
  "name": "资金转移限制规则",
  "contractAddress": "0x1234567890abcdef1234567890abcdef12345678",
  "description": "限制单次转账金额不超过1000 ETH",
  "owner": "super",
  "functionName": "transfer",
  "parameters": "[{\"name\":\"amount\",\"value\":\"1000\",\"type\":\"uint256\"}]"
}
```

**响应数据**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": 2,
    "name": "资金转移限制规则",
    "regulatorAddress": "0x1234567890abcdef1234567890abcdef12345678",
    "description": "限制单次转账金额不超过1000 ETH",
    "contractAddress": "0x1234567890abcdef1234567890abcdef12345678",
    "owner": "super",
    "ruleId": "RULE20240306002",
    "status": 0,
    "createTime": "2024-03-06 15:30:00"
  }
}
```

### 3. 更新规则

**接口说明**: 更新现有监管规则  
**调用位置**: `src/views/RuleManagement/index.vue` 的 `handleSubmit` 方法（当 `dialogType === 'edit'` 时）  
**请求方法**: PUT  
**请求路径**: `/api/rules/:id`  
**请求类型**: multipart/form-data  

**请求参数**:
```typescript
{
  name?: string          // 规则名称（可选）
  contractAddress?: string   // 合约地址（可选）
  description?: string  // 规则描述（可选）
  functionName?: string // 函数名称（可选）
  parameters?: string   // JSON字符串格式的参数列表（可选）
  file?: File          // 规则文件（可选）
}
```

**响应数据**:
```json
{
  "code": 200,
  "message": "success"
}
```

### 4. 删除规则

**接口说明**: 删除指定监管规则  
**调用位置**: `src/views/RuleManagement/index.vue` 的 `handleDelete` 方法  
**请求方法**: DELETE  
**请求路径**: `/api/rules/:id`  

**响应数据**:
```json
{
  "code": 200,
  "message": "success"
}
```

## 合约管理接口

### 1. 获取已部署合约列表

**接口说明**: 获取系统中已部署的合约列表  
**调用位置**: `src/views/RuleManagement/index.vue` 的已部署合约列表区域  
**请求方法**: GET  
**请求路径**: `/api/contracts`  

**请求参数**:
```typescript
{
  keyword?: string    // 搜索关键词（可选）
}
```

**响应数据**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "list": [
      {
        "id": 1,
        "name": "TokenContract",
        "address": "0x1234567890abcdef1234567890abcdef12345678",
        "sourceCode": "contract TokenContract {\n    uint256 public totalSupply;\n    \n    function store(uint256 num) public {\n        totalSupply = num;\n    }\n}"
      }
    ]
  }
}
```

## 状态码说明

| 状态码 | 说明 |
|--------|------|
| 200    | 成功 |
| 400    | 请求参数错误 |
| 401    | 未授权 |
| 403    | 权限不足 |
| 404    | 资源不存在 |
| 500    | 服务器内部错误 |

## 注意事项

1. 所有涉及地址的字段必须是有效的以太坊地址格式（0x开头的40位十六进制字符）
2. 文件上传支持的格式为：.sol、.txt、.json
3. 参数列表必须是有效的JSON字符串
4. 所有时间字段使用ISO 8601格式
5. 分页参数page从1开始计数 