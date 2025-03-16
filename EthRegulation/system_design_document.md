# 监管规则管理系统设计文档

## 1. 系统概述

监管规则管理系统是一个用于管理区块链智能合约监管规则的应用程序。它允许用户创建、编辑、删除和查看针对不同智能合约的监管规则，并关联规则与特定合约函数。

## 2. 前端设计

### 2.1 页面结构

#### 2.1.1 规则管理页面（主页面）

- 功能：展示所有监管规则列表，支持搜索、排序、筛选和分页
- 组件：
  - 搜索框：按名称或合约地址搜索规则
  - 规则表格：展示规则详细信息
  - 操作按钮：新增、编辑、删除规则
  - 分页控件：控制表格页码和每页展示数量

#### 2.1.2 新增/编辑规则对话框

- 功能：创建新规则或编辑现有规则
- 组件：
  - 表单：包含规则名称、合约地址、描述、拥有者等字段
  - 合约选择器：选择要关联的智能合约
  - 函数配置区域：配置规则适用的合约函数和参数
  - 源码预览区域：展示合约源码
  - 监管账户地址选择器：选择监管账户地址

#### 2.1.3 合约选择器对话框

- 功能：浏览和选择已部署的智能合约
- 组件：
  - 合约列表：展示所有可选合约
  - 搜索和过滤功能：筛选合约
  - 源码预览：查看合约源码
  - 分页控件：控制列表页码

### 2.2 主要组件设计

#### 2.2.1 规则表格

\`\`\`vue
<el-table :data="tableData" border style="width: 100%" v-loading="loading">
  <el-table-column type="index" label="序号" width="70" />
  <el-table-column prop="ruleId" label="监管规则编号" min-width="150" sortable />
  <el-table-column prop="contractAddress" label="监管合约地址" min-width="300" sortable />
  <el-table-column prop="name" label="规则名称" min-width="200" sortable />
  <el-table-column prop="regulatorAddress" label="监管账户地址" min-width="300" />
  <el-table-column prop="description" label="规则描述" min-width="200" />
  <el-table-column prop="createTime" label="创建时间" min-width="180" sortable />
  <el-table-column label="操作" fixed="right" width="160">
    <!-- 操作按钮：编辑、删除 -->
  </el-table-column>
</el-table>
\`\`\`

#### 2.2.2 规则表单

\`\`\`vue
<el-form ref="formRef" :model="form" :rules="rules" label-width="120px">
  <el-form-item label="规则名称" prop="name">
    <el-input v-model="form.name" placeholder="请输入规则名称" />
  </el-form-item>
  <el-form-item label="合约地址" prop="contractAddress">
    <el-input 
      v-model="form.contractAddress" 
      placeholder="请选择合约" 
      :readonly="isEdit"
      :disabled="isEdit"
    />
    <el-button @click="openContractSelector" :disabled="isEdit">选择合约</el-button>
  </el-form-item>
  <el-form-item label="监管账户地址" prop="regulatorAddress">
    <div class="regulator-address-container">
      <el-input v-model="form.regulatorAddress" placeholder="请输入监管账户地址" />
      <!-- 监管账户地址下拉选择器 -->
    </div>
  </el-form-item>
  <el-form-item label="规则描述" prop="description">
    <el-input v-model="form.description" type="textarea" rows="3" />
  </el-form-item>
  <el-form-item label="创建者" prop="owner">
    <el-input v-model="form.owner" placeholder="请输入创建者" />
  </el-form-item>
  
  <!-- 函数配置区域 -->
  <div v-for="(func, funcIndex) in form.functions" :key="funcIndex" class="function-config">
    <!-- 函数名称、参数配置 -->
  </div>
</el-form>
\`\`\`

#### 2.2.3 合约选择器

\`\`\`vue
<div class="contract-selector-content">
  <!-- 左侧合约列表 -->
  <div class="contract-list">
    <el-table :data="filteredContracts" border @row-click="previewContract">
      <el-table-column prop="name" label="合约名称" />
      <el-table-column prop="address" label="合约地址" />
      <el-table-column prop="createTime" label="部署时间" />
      <el-table-column label="操作">
        <template #default="{ row }">
          <el-button type="primary" @click.stop="selectContract(row)">选择</el-button>
          <el-button @click.stop="previewContract(row)">预览源码</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
  
  <!-- 右侧源码预览 -->
  <div v-if="previewingContract" class="contract-preview">
    <!-- 合约源码预览区域 -->
  </div>
</div>
\`\`\`

## 3. 后端设计

### 3.1 数据库模型

#### 3.1.1 Rule 模型

\`\`\`python
class RuleNew(db.Model):
    __tablename__ = 'rules_new'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    contract_address = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    owner = db.Column(db.String(255))
    functions = db.Column(db.JSON)
    status = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    update_time = db.Column(db.DateTime, onupdate=datetime.utcnow)
    rule_number = db.Column(db.String(255), unique=True)
    regulator_address = db.Column(db.String(255))
\`\`\`

#### 3.1.2 Contract 模型

\`\`\`python
class Contract(db.Model):
    __tablename__ = 'contracts'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False, unique=True)
    source_code = db.Column(db.Text)
    abi = db.Column(db.JSON)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.Integer, default=1)
\`\`\`

### 3.2 API设计

#### 3.2.1 规则管理API

| 端点 | 方法 | 描述 | 参数 | 返回值 |
|------|------|------|------|--------|
| \`/api/rules\` | GET | 获取规则列表 | page, pageSize, keyword | 规则列表、总数 |
| \`/api/rules\` | POST | 创建新规则 | 规则数据 | 创建的规则详情 |
| \`/api/rules/<id>\` | GET | 获取规则详情 | id | 规则详情 |
| \`/api/rules/<id>\` | PUT | 更新规则 | id, 规则数据 | 更新后的规则详情 |
| \`/api/rules/<id>\` | DELETE | 删除规则 | id | 成功消息 |

#### 3.2.2 合约管理API

| 端点 | 方法 | 描述 | 参数 | 返回值 |
|------|------|------|------|--------|
| \`/api/contracts\` | GET | 获取合约列表 | 无 | 合约列表、总数 |
| \`/api/contracts/<address>\` | GET | 获取合约详情 | address | 合约详情 |

### 3.3 API实现细节

#### 3.3.1 获取规则列表

\`\`\`python
@bp.route('/api/rules', methods=['GET'])
def get_rules():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    keyword = request.args.get('keyword', '')
    
    query = RuleNew.query
    if keyword:
        query = query.filter(
            (RuleNew.name.ilike(f'%{keyword}%')) |
            (RuleNew.contract_address.ilike(f'%{keyword}%'))
        )
    
    total = query.count()
    items = query.order_by(RuleNew.id.desc())\
        .offset((page - 1) * page_size)\
        .limit(page_size)\
        .all()
    
    return {
        'code': 200,
        'message': 'success',
        'data': {
            'list': rules_schema.dump(items),
            'total': total,
            'page': page,
            'pageSize': page_size
        }
    }
\`\`\`

#### 3.3.2 创建规则

\`\`\`python
@bp.route('/api/rules', methods=['POST'])
def create_rule():
    try:
        data = request.get_json()
        
        # 生成规则编号 R-年份-合约后4位-时间戳-序号
        current_time = datetime.now()
        year = current_time.strftime('%y')
        timestamp = current_time.strftime('%H%M')
        
        contract_address = data['contractAddress']
        contract_suffix = contract_address[-4:] if contract_address else 'XXXX'
        
        today_rules = RuleNew.query.filter(
            db.func.date(RuleNew.create_time) == db.func.date(current_time)
        ).all()
        sequence = str(len(today_rules) + 1).zfill(3)
        
        rule_number = f"R-{year}-{contract_suffix}-{timestamp}-{sequence}"
        
        rule = RuleNew(
            name=data['name'],
            contract_address=contract_address,
            description=data.get('description'),
            owner=data['owner'],
            functions=data['functions'],
            regulator_address=data.get('regulatorAddress'),
            rule_number=rule_number,
            create_time=current_time
        )
        
        db.session.add(rule)
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'message': 'success',
            'data': rule_schema.dump(rule)
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 400,
            'message': str(e)
        }), 400
\`\`\`

#### 3.3.3 获取合约详情

\`\`\`python
@bp.route('/api/contracts/<address>', methods=['GET'])
def get_contract(address):
    contract = Contract.query.filter_by(address=address).first_or_404()
    return jsonify({
        'code': 200,
        'message': 'success',
        'data': contract_schema.dump(contract)
    })
\`\`\`

## 4. 前后端交互流程

### 4.1 规则列表加载流程

1. 用户访问规则管理页面
2. 前端调用 \`/api/rules\` 接口获取规则列表
3. 后端查询数据库并返回规则数据
4. 前端渲染规则表格

### 4.2 新增规则流程

1. 用户点击"新增规则"按钮
2. 弹出新增规则对话框
3. 用户填写规则信息和选择合约
   - 选择合约时，打开合约选择器对话框
   - 前端调用 \`/api/contracts\` 获取合约列表
   - 用户选择合约后，前端调用 \`/api/contracts/{address}\` 获取合约详情
   - 前端解析合约源码，提取函数列表供用户选择
4. 用户配置规则函数和参数
5. 用户提交表单，前端调用 \`/api/rules\` POST 接口
6. 后端生成唯一规则编号，创建新规则并保存
7. 后端返回完整规则数据，前端显示成功提示并刷新列表

### 4.3 编辑规则流程

1. 用户点击规则行的"编辑"按钮
2. 弹出编辑规则对话框，前端显示规则现有数据
3. 用户修改规则信息（合约地址不可修改）
4. 用户提交表单，前端调用 \`/api/rules/{id}\` PUT 接口
5. 后端更新规则并返回更新后的数据
6. 前端显示成功提示并刷新列表

## 5. 特殊功能实现

### 5.1 规则编号生成

- 格式：R-年份-合约后4位-时间戳-序号
- 实现方式：
  - 年份：当前年份的后两位（如 25 代表 2025 年）
  - 合约后4位：使用合约地址的最后 4 个字符
  - 时间戳：创建时间的小时和分钟（如 1422 代表 14:22）
  - 序号：当天的序号，从 001 开始
- 唯一性保证：使用创建时间和序号确保唯一性

### 5.2 函数参数配置

- 用户选择合约后，系统自动解析合约中的函数
- 用户可以为每个函数配置监管规则的参数
- 参数包括名称、类型、条件和监管值
- 支持动态添加多个函数和参数

### 5.3 监管账户地址选择

- 用户可以从下拉列表中选择已有的监管账户地址
- 也可以直接输入新的监管账户地址
- 系统会自动从已有规则中提取监管账户地址供用户选择

## 6. 安全性考虑

- 输入验证：对所有用户输入进行验证，防止恶意输入
- 访问控制：确保只有授权用户才能执行敏感操作
- 异常处理：所有操作都包含适当的异常处理机制
- 数据完整性：确保规则编号等关键字段的唯一性
- 安全日志：记录所有重要操作，便于审计

## 7. 扩展性设计

系统设计支持未来扩展：
- 新增监管规则类型
- 增加更复杂的规则条件
- 支持更多类型的智能合约和区块链平台
- 集成自动化测试和验证工具
- 添加监管规则执行和监控功能
