# 监管规则配置 API 文档

## 1. 规则列表接口

### 1.1 获取规则列表

- **接口地址**：`/api/v1/rules`
- **请求方式**：`GET`
- **分页方式**：后端分页
- **请求参数**：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| page | number | 是 | 当前页码，从1开始 |
| pageSize | number | 是 | 每页条数 |
| keyword | string | 否 | 搜索关键词（规则名称或合约地址） |
| status | number | 否 | 规则状态（0-待审核，1-已上线，2-已下线） |
| sortField | string | 否 | 排序字段 |
| sortOrder | string | 否 | 排序方向（asc/desc） |

- **请求示例**：
```http
GET /api/v1/rules?page=1&pageSize=10&keyword=transfer&status=1&sortField=createTime&sortOrder=desc
```

- **响应参数**：

| 参数名 | 类型 | 说明 |
|--------|------|------|
| code | number | 状态码 |
| message | string | 提示信息 |
| data | object | 响应数据 |
| data.total | number | 总条数 |
| data.list | array | 规则列表 |

- **响应示例**：
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "total": 50,
    "list": [
      {
        "id": 1,
        "ruleId": "RULE20240306001",
        "name": "转账限制规则",
        "description": "限制单次转账金额不超过1000 ETH",
        "contractAddress": "0x1234567890abcdef1234567890abcdef12345678",
        "regulatorAddress": "0xabcdef1234567890abcdef1234567890abcdef12",
        "owner": "super",
        "status": 1,
        "createTime": "2024-03-06T10:00:00Z",
        "functions": [
          {
            "name": "transfer",
            "params": [
              {
                "name": "amount",
                "type": "uint256",
                "condition": "<=",
                "value": "1000000000000000000000"
              }
            ]
          }
        ]
      },
      {
        "id": 2,
        "ruleId": "RULE20240306002",
        "name": "交易时间限制",
        "description": "限制交易时间在工作日9:00-18:00",
        "contractAddress": "0x2345678901abcdef2345678901abcdef23456789",
        "regulatorAddress": "0xbcdef1234567890abcdef1234567890abcdef123",
        "owner": "super",
        "status": 0,
        "createTime": "2024-03-06T09:30:00Z",
        "functions": [
          {
            "name": "trade",
            "params": [
              {
                "name": "timestamp",
                "type": "uint256",
                "condition": "in_range",
                "value": "32400,64800"
              }
            ]
          }
        ]
      }
    ]
  }
}
```

### 1.2 删除规则

- **接口地址**：`/api/v1/rules/{ruleId}`
- **请求方式**：`DELETE`
- **请求参数**：无（参数在URL中）

- **响应示例**：
```json
{
  "code": 0,
  "message": "删除成功",
  "data": null
}
```

## 2. 规则管理接口

### 2.1 创建规则

- **接口地址**：`/api/v1/rules`
- **请求方式**：`POST`
- **请求参数**：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| name | string | 是 | 规则名称 |
| description | string | 是 | 规则描述 |
| contractAddress | string | 是 | 合约地址 |
| functions | array | 是 | 函数规则列表 |

- **请求示例**：
```json
{
  "name": "新转账限制规则",
  "description": "限制单次转账金额不超过500 ETH",
  "contractAddress": "0x3456789012abcdef3456789012abcdef34567890",
  "functions": [
    {
      "name": "transfer",
      "params": [
        {
          "name": "amount",
          "type": "uint256",
          "condition": "<=",
          "value": "500000000000000000000"
        }
      ]
    }
  ]
}
```

- **响应示例**：
```json
{
  "code": 0,
  "message": "创建成功",
  "data": {
    "id": 3,
    "ruleId": "RULE20240306003",
    "name": "新转账限制规则",
    "description": "限制单次转账金额不超过500 ETH",
    "contractAddress": "0x3456789012abcdef3456789012abcdef34567890",
    "regulatorAddress": "0xcdef1234567890abcdef1234567890abcdef1234",
    "owner": "super",
    "status": 0,
    "createTime": "2024-03-06T11:00:00Z",
    "functions": [
      {
        "name": "transfer",
        "params": [
          {
            "name": "amount",
            "type": "uint256",
            "condition": "<=",
            "value": "500000000000000000000"
          }
        ]
      }
    ]
  }
}
```

### 2.2 更新规则

- **接口地址**：`/api/v1/rules/{ruleId}`
- **请求方式**：`PUT`
- **请求参数**：同创建规则

- **响应示例**：
```json
{
  "code": 0,
  "message": "更新成功",
  "data": {
    "id": 3,
    "ruleId": "RULE20240306003",
    "name": "更新后的规则名称",
    "description": "更新后的规则描述",
    "contractAddress": "0x3456789012abcdef3456789012abcdef34567890",
    "regulatorAddress": "0xcdef1234567890abcdef1234567890abcdef1234",
    "owner": "super",
    "status": 0,
    "createTime": "2024-03-06T11:00:00Z",
    "updateTime": "2024-03-06T11:30:00Z",
    "functions": [
      {
        "name": "transfer",
        "params": [
          {
            "name": "amount",
            "type": "uint256",
            "condition": "<=",
            "value": "600000000000000000000"
          }
        ]
      }
    ]
  }
}
```

## 3. 合约相关接口

### 3.1 获取合约列表

- **接口地址**：`/api/v1/contracts`
- **请求方式**：`GET`
- **分页方式**：后端分页
- **请求参数**：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| page | number | 是 | 当前页码 |
| pageSize | number | 是 | 每页条数 |
| keyword | string | 否 | 搜索关键词（合约名称或地址） |

- **响应示例**：
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "total": 100,
    "list": [
      {
        "id": 1,
        "name": "TokenContractV1",
        "address": "0x4567890123abcdef4567890123abcdef45678901",
        "createTime": "2024-03-01T10:00:00Z",
        "sourceCode": "contract TokenContractV1 {\n    // 合约源码\n}",
        "functions": ["transfer", "mint", "burn"]
      },
      {
        "id": 2,
        "name": "TradeContractV2",
        "address": "0x5678901234abcdef5678901234abcdef56789012",
        "createTime": "2024-03-02T14:30:00Z",
        "sourceCode": "contract TradeContractV2 {\n    // 合约源码\n}",
        "functions": ["trade", "cancel", "withdraw"]
      }
    ]
  }
}
```

### 3.2 获取合约详情

- **接口地址**：`/api/v1/contracts/{address}`
- **请求方式**：`GET`
- **请求参数**：无（参数在URL中）

- **响应示例**：
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": 1,
    "name": "TokenContractV1",
    "address": "0x4567890123abcdef4567890123abcdef45678901",
    "createTime": "2024-03-01T10:00:00Z",
    "sourceCode": "contract TokenContractV1 {\n    // State variables\n    address public owner;\n    uint256 public totalSupply;\n    mapping(address => uint256) public balances;\n    \n    // Events\n    event Transfer(address indexed from, address indexed to, uint256 value);\n    \n    constructor() {\n        owner = msg.sender;\n    }\n    \n    // Main functions\n    function transfer(address to, uint256 amount) public {\n        require(balances[msg.sender] >= amount, \"Insufficient balance\");\n        balances[msg.sender] -= amount;\n        balances[to] += amount;\n        emit Transfer(msg.sender, to, amount);\n    }\n    \n    function mint(address to, uint256 amount) public {\n        require(msg.sender == owner, \"Only owner can mint\");\n        totalSupply += amount;\n        balances[to] += amount;\n        emit Transfer(address(0), to, amount);\n    }\n}",
    "functions": [
      {
        "name": "transfer",
        "params": [
          {
            "name": "to",
            "type": "address"
          },
          {
            "name": "amount",
            "type": "uint256"
          }
        ],
        "returns": []
      },
      {
        "name": "mint",
        "params": [
          {
            "name": "to",
            "type": "address"
          },
          {
            "name": "amount",
            "type": "uint256"
          }
        ],
        "returns": []
      }
    ]
  }
}
```

## 4. 数据规范说明

### 4.1 分页处理
- 所有列表接口均采用后端分页
- 前端传入 page（当前页码）和 pageSize（每页条数）
- 后端返回 total（总条数）和当前页数据

### 4.2 排序和筛选
- 表格排序：后端实现，前端传入 sortField 和 sortOrder
- 表格筛选：前端实现，使用本地数据过滤

### 4.3 状态码规范
```json
{
  "0": "成功",
  "1001": "参数错误",
  "1002": "未授权",
  "1003": "资源不存在",
  "1004": "操作失败",
  "5000": "系统错误"
}
```

### 4.4 时间格式
- 所有时间字段统一使用 ISO 8601 格式
- 示例：`2024-03-06T10:00:00Z`

### 4.5 地址格式
- 所有地址字段统一使用 40 位十六进制字符串，前缀 "0x"
- 示例：`0x1234567890abcdef1234567890abcdef12345678`

### 4.6 数值格式
- 金额类数值使用字符串类型，避免精度丢失
- 示例：`"1000000000000000000000"`（1000 ETH） 