<template>
  <div class="rule-management">
    <!-- 搜索和操作区域 -->
    <div class="operation-bar">
      <div class="left">
        <el-input
          v-model="searchQuery"
          placeholder="请输入规则名称或被监管合约地址"
          style="width: 300px"
          clearable
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
      </div>
      <div class="right">
        <el-button type="primary" @click="handleSearch">查询</el-button>
        <el-button @click="handleReset">重置</el-button>
        <el-button type="success" @click="handleAdd">
          <el-icon><Plus /></el-icon>
          新增规则
        </el-button>
      </div>
    </div>

    <!-- 表格区域 -->
    <el-table 
      :data="tableData" 
      border 
      style="width: 100%"
      v-loading="loading"
    >
      <el-table-column type="index" label="序号" width="80" />
      <el-table-column prop="name" label="规则名称" min-width="150" sortable :filters="getColumnFilters('name')" :filter-method="filterHandler" />
      <el-table-column prop="regulatorAddress" label="监管账户地址" min-width="200" sortable :filters="getColumnFilters('regulatorAddress')" :filter-method="filterHandler" />
      <el-table-column prop="description" label="简介" min-width="200" show-overflow-tooltip />
      <el-table-column prop="contractAddress" label="被监管合约地址" min-width="200" sortable :filters="getColumnFilters('contractAddress')" :filter-method="filterHandler">
        <template #default="{ row }">
          <el-button link type="primary" @click="viewContract(row)">
            {{ row.contractAddress }}
          </el-button>
        </template>
      </el-table-column>
      <el-table-column prop="owner" label="所属用户" min-width="120" sortable :filters="getColumnFilters('owner')" :filter-method="filterHandler" />
      <el-table-column prop="ruleId" label="监管规则编号" min-width="150" sortable :filters="getColumnFilters('ruleId')" :filter-method="filterHandler" />
      <el-table-column prop="status" label="状态" width="100" sortable :filters="[
        { text: '待审核', value: 0 },
        { text: '已上线', value: 1 },
        { text: '已下线', value: 2 }
      ]" :filter-method="filterHandler">
        <template #default="{ row }">
          <el-tag :type="getStatusType(row.status)">
            {{ getStatusText(row.status) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="createTime" label="创建时间" min-width="180" sortable>
        <template #default="{ row }">
          {{ formatDate(row.createTime) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <el-button link type="primary" @click="handleEdit(row)">编辑</el-button>
          <el-button link type="danger" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页器 -->
    <div class="pagination-container">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[10, 20, 50, 100]"
        :total="total"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>

    <!-- 新增/编辑规则对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑规则' : '新增规则'"
      width="80%"
      :close-on-click-modal="false"
    >
      <div class="dialog-content">
        <!-- 左侧表单 -->
        <div class="form-section">
          <el-form
            ref="formRef"
            :model="form"
            :rules="rules"
            label-width="120px"
            class="rule-form"
          >
            <el-form-item label="规则名称" prop="name">
              <el-input v-model="form.name" placeholder="请输入规则名称" />
            </el-form-item>
            
            <el-form-item label="被监管合约" prop="contractAddress">
              <el-input
                v-model="selectedContractName"
                placeholder="请选择合约"
                readonly
                @click="showContractSelector"
              >
                <template #append>
                  <el-button @click="showContractSelector">选择合约</el-button>
                </template>
              </el-input>
            </el-form-item>

            <el-form-item label="简介" prop="description">
              <el-input
                v-model="form.description"
                type="textarea"
                :rows="3"
                placeholder="请输入规则简介"
              />
            </el-form-item>

            <!-- 函数规则部分 -->
            <div v-for="(func, funcIndex) in form.functions" :key="funcIndex" class="function-section">
              <div class="function-header">
                <h3>函数 {{ funcIndex + 1 }}</h3>
                <el-button type="danger" circle @click="removeFunction(funcIndex)">
                  <el-icon><Delete /></el-icon>
                </el-button>
              </div>

              <el-form-item :label="'函数名称'" :prop="'functions.' + funcIndex + '.name'">
                <el-select
                  v-model="func.name"
                  placeholder="请选择函数"
                  style="width: 100%"
                >
                  <el-option
                    v-for="fn in contractFunctions"
                    :key="fn"
                    :label="fn"
                    :value="fn"
                  />
                </el-select>
              </el-form-item>

              <!-- 参数列表 -->
              <div v-for="(param, paramIndex) in func.params" :key="paramIndex" class="param-item">
                <el-form-item 
                  :label="'参数 ' + (paramIndex + 1)"
                  :prop="'functions.' + funcIndex + '.params.' + paramIndex + '.value'"
                >
                  <div class="param-row">
                    <el-input
                      v-model="param.name"
                      placeholder="参数名称"
                      style="width: 150px"
                    />
                    <el-select
                      v-model="param.type"
                      placeholder="参数类型"
                      style="width: 120px"
                    >
                      <el-option label="uint256" value="uint256" />
                      <el-option label="string" value="string" />
                      <el-option label="address" value="address" />
                      <el-option label="bool" value="bool" />
                    </el-select>
                    <el-select
                      v-model="param.condition"
                      placeholder="条件"
                      style="width: 120px"
                    >
                      <el-option label="等于" value="=" />
                      <el-option label="大于" value=">" />
                      <el-option label="大于等于" value=">=" />
                      <el-option label="小于" value="<" />
                      <el-option label="小于等于" value="<=" />
                      <el-option label="不等于" value="!=" />
                      <el-option label="包含" value="includes" />
                      <el-option label="不包含" value="not_includes" />
                      <el-option label="在范围内" value="in_range" />
                      <el-option label="不在范围内" value="not_in_range" />
                    </el-select>
                    <el-input
                      v-model="param.value"
                      placeholder="参数值"
                      style="width: 200px"
                    />
                    <el-button type="danger" @click="removeParam(funcIndex, paramIndex)">
                      <el-icon><Delete /></el-icon>
                      删除
                    </el-button>
                  </div>
                </el-form-item>
              </div>

              <el-button type="primary" @click="addParam(funcIndex)">
                <el-icon><Plus /></el-icon>
                添加参数
              </el-button>
            </div>

            <el-button type="primary" @click="addFunction">
              <el-icon><Plus /></el-icon>
              添加函数
            </el-button>
          </el-form>
        </div>

        <!-- 右侧合约源码 -->
        <div v-if="selectedContract" class="contract-section">
          <div class="contract-header">
            <h3>合约源码</h3>
            <p class="contract-info">
              <span>名称：{{ selectedContract.name }}</span>
              <span>地址：{{ selectedContract.address }}</span>
            </p>
          </div>
          <div class="source-code">
            <pre class="language-solidity"><code>{{ selectedContract.sourceCode }}</code></pre>
          </div>
        </div>
      </div>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 查看合约详情对话框 -->
    <el-dialog
      v-model="contractDialogVisible"
      title="合约详情"
      width="80%"
      class="contract-dialog"
    >
      <div class="contract-detail">
        <div class="contract-info">
          <h3>基本信息</h3>
          <el-descriptions :column="2" border>
            <el-descriptions-item label="合约名称">{{ selectedContract?.name }}</el-descriptions-item>
            <el-descriptions-item label="合约地址">{{ selectedContract?.address }}</el-descriptions-item>
            <el-descriptions-item label="创建时间">{{ formatDate(selectedContract?.createTime) }}</el-descriptions-item>
            <el-descriptions-item label="状态">
              <el-tag>已部署</el-tag>
            </el-descriptions-item>
          </el-descriptions>
        </div>
        
        <div class="contract-source">
          <h3>源代码</h3>
          <div class="code-wrapper">
            <pre class="language-solidity"><code>{{ selectedContract?.sourceCode }}</code></pre>
          </div>
        </div>

        <div class="contract-functions">
          <h3>可用函数</h3>
          <el-table :data="contractFunctions" border style="width: 100%">
            <el-table-column prop="name" label="函数名称" />
            <el-table-column prop="params" label="参数" />
            <el-table-column prop="returns" label="返回值" />
          </el-table>
        </div>
      </div>
    </el-dialog>

    <!-- 选择合约对话框 -->
    <el-dialog
      v-model="contractSelectorVisible"
      title="选择合约"
      width="90%"
    >
      <div class="contract-selector">
        <div class="search-bar">
          <el-input
            v-model="contractSearchQuery"
            placeholder="搜索合约名称或地址"
            clearable
            @input="handleContractSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </div>
        
        <div class="contract-selector-content">
          <!-- 左侧合约列表 -->
          <div class="contract-list">
            <el-table
              :data="filteredContracts"
              border
              style="width: 100%"
              height="500"
              @row-click="previewContract"
            >
              <el-table-column prop="name" label="合约名称" min-width="150" />
              <el-table-column prop="address" label="合约地址" min-width="300" />
              <el-table-column prop="createTime" label="部署时间" min-width="180">
                <template #default="{ row }">
                  {{ formatDate(row.createTime) }}
                </template>
              </el-table-column>
              <el-table-column label="操作" width="260" fixed="right">
                <template #default="{ row }">
                  <el-button type="primary" @click.stop="selectContract(row)">
                    选择
                  </el-button>
                  <el-button 
                    :type="previewingContract?.address === row.address ? 'success' : 'info'"
                    @click.stop="previewContract(row)"
                  >
                    {{ previewingContract?.address === row.address ? '正在预览' : '预览源码' }}
                  </el-button>
                </template>
              </el-table-column>
            </el-table>

            <div class="pagination">
              <el-pagination
                v-model:current-page="contractPage"
                v-model:page-size="contractPageSize"
                :total="filteredContracts.length"
                :page-sizes="[10, 20, 50, 100]"
                layout="total, sizes, prev, pager, next"
                @size-change="handleContractSizeChange"
                @current-change="handleContractPageChange"
              />
            </div>
          </div>

          <!-- 右侧源码预览 -->
          <div v-if="previewingContract" class="contract-preview">
            <div class="preview-header">
              <h3>合约源码预览</h3>
              <p class="contract-info">
                <span>名称：{{ previewingContract.name }}</span>
                <span>地址：{{ previewingContract.address }}</span>
              </p>
            </div>
            <div class="preview-content">
              <pre class="language-solidity"><code>{{ previewingContract.sourceCode }}</code></pre>
            </div>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search, Plus, Delete } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import { getRuleList, addRule, updateRule, deleteRule } from '@/api/rules'
import useStoreUser from '@/store/user'

const router = useRouter()
const storeUser = useStoreUser()

// 使用空数组初始化
const contracts = ref([]);

// 响应式状态
const searchQuery = ref('')
const tableData = ref([])  // 改为空数组
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)  // 改为 0
const dialogVisible = ref(false)
const contractDialogVisible = ref(false)
const selectedContract = ref<any>(null)
const isEdit = ref(false)
const contractFunctions = ref(['transfer', 'mint', 'trade'])

// 表单数据
const form = ref({
  id: '',
  name: '',
  contractAddress: '',
  description: '',
  owner: 'super',
  functions: [] as Array<{
    name: string
    params: Array<{
      name: string
      type: string
      condition: string
      value: string
    }>
  }>
})

// 表单规则
const rules = {
  name: [{ required: true, message: '请输入规则名称', trigger: 'blur' }],
  contractAddress: [{ required: true, message: '请选择合约', trigger: 'change' }],
  description: [{ required: true, message: '请输入规则简介', trigger: 'blur' }]
}

// 状态相关
const getStatusType = (status: number): 'success' | 'warning' | 'info' => {
  const types = {
    0: 'info',    // 待审核
    1: 'success', // 已上线
    2: 'warning'  // 已下线
  }
  return types[status] as 'success' | 'warning' | 'info'
}

const getStatusText = (status: number) => {
  const texts = {
    0: '待审核',
    1: '已上线',
    2: '已下线'
  }
  return texts[status] || '未知'
}

// 日期格式化
const formatDate = (dateStr: string) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false
  })
}

// 事件处理
const handleSearch = async () => {
  loading.value = true
  try {
    const [err, res] = await getRuleList({
      page: currentPage.value,
      pageSize: pageSize.value,
      keyword: searchQuery.value
    })
    if (!err && res.code === 200) {
      tableData.value = res.data.list
      total.value = res.data.total
    } else {
      ElMessage.error(err?.message || '获取数据失败')
      /* 注释掉 Mock 数据回退
      tableData.value = mockData
      total.value = mockData.length
      */
    }
  } finally {
    loading.value = false
  }
}

const handleReset = () => {
  searchQuery.value = ''
  currentPage.value = 1
  handleSearch()
}

const handleSizeChange = (val: number) => {
  pageSize.value = val
  handleSearch()
}

const handleCurrentChange = (val: number) => {
  currentPage.value = val
  handleSearch()
}

const handleAdd = () => {
  isEdit.value = false
  
  // 默认选择第一个合约
  const defaultContract = contracts.value[0]
  
  form.value = {
    id: '',
    name: '',
    contractAddress: defaultContract.address,
    description: '',
    owner: 'super',
    functions: [{  // 默认添加一个空函数
      name: '',
      params: []
    }]
  }
  
  // 设置选中的合约名称和预览
  selectedContractName.value = `${defaultContract.name} (${defaultContract.address})`
  selectedContract.value = defaultContract
  
  dialogVisible.value = true
  
  // 触发代码高亮
  nextTick(() => {
    highlightCode()
  })
}

const handleEdit = (row: any) => {
  isEdit.value = true
  form.value = JSON.parse(JSON.stringify(row))
  dialogVisible.value = true
  // 加载合约详情
  const contract = contracts.value.find(c => c.address === row.contractAddress)
  if (contract) {
    selectedContract.value = contract
    highlightCode()
  }
}

const viewContract = (row: any) => {
  const contract = contracts.value.find(c => c.address === row.contractAddress)
  if (contract) {
    selectedContract.value = contract
    contractDialogVisible.value = true
    highlightCode()
  }
}

const handleDelete = async (row: any) => {
  try {
    await ElMessageBox.confirm(
      '确认删除该规则吗？此操作将不可恢复',
      '删除确认',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    const [err, res] = await deleteRule(row.id)
    if (!err && res.code === 200) {
      ElMessage.success('删除成功')
      handleSearch() // 重新加载数据
    } else {
      ElMessage.error(err?.message || '删除失败')
    }
  } catch (error) {
    console.error('删除失败:', error)
  }
}

// 函数规则相关
const addFunction = () => {
  form.value.functions.push({
    name: '',
    params: []
  })
}

const removeFunction = (index: number) => {
  form.value.functions.splice(index, 1)
}

const addParam = (funcIndex: number) => {
  form.value.functions[funcIndex].params.push({
    name: '',
    type: 'uint256',
    condition: '=',
    value: ''
  })
}

const removeParam = (funcIndex: number, paramIndex: number) => {
  form.value.functions[funcIndex].params.splice(paramIndex, 1)
}

const handleContractSelect = (address: string) => {
  const contract = contracts.value.find(c => c.address === address)
  if (contract) {
    selectedContract.value = contract
  }
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    
    // 构建要发送的数据
    const formData = new FormData()
    formData.append('name', form.value.name)
    formData.append('contractAddress', form.value.contractAddress)
    formData.append('description', form.value.description)
    formData.append('owner', form.value.owner)
    formData.append('functions', JSON.stringify(form.value.functions))
    
    console.log('Submitting data:', {
      id: form.value.id,
      formData: Object.fromEntries(formData.entries())
    })

    const res = form.value.id 
      ? await updateRule(form.value.id, formData)
      : await addRule(formData)

    console.log('Response:', res)

    if (res.code === 200) {
      ElMessage.success(form.value.id ? '更新成功' : '添加成功')
      dialogVisible.value = false
      await fetchData()
    } else {
      ElMessage.error(res.message || '操作失败')
    }
  } catch (error) {
    console.error('提交失败:', error)
    ElMessage.error('操作失败，请重试')
  }
}

// 合约选择相关
const contractSelectorVisible = ref(false)
const contractSearchQuery = ref('')
const contractPage = ref(1)
const contractPageSize = ref(10)
const selectedContractName = ref('')
const filteredContracts = ref(contracts.value)

const showContractSelector = () => {
  contractSelectorVisible.value = true
  contractSearchQuery.value = ''
  filteredContracts.value = contracts.value
}

const handleContractSearch = () => {
  const query = contractSearchQuery.value.toLowerCase()
  filteredContracts.value = contracts.value.filter(contract => 
    contract.name.toLowerCase().includes(query) ||
    contract.address.toLowerCase().includes(query)
  )
}

const handleContractSizeChange = (val: number) => {
  contractPageSize.value = val
}

const handleContractPageChange = (val: number) => {
  contractPage.value = val
}

const selectContract = (contract: any) => {
  form.value.contractAddress = contract.address
  selectedContractName.value = `${contract.name} (${contract.address})`
  selectedContract.value = contract
  contractSelectorVisible.value = false
  highlightCode()
}

// 合约预览相关
const previewingContract = ref<any>(null)

const previewContract = (contract: any) => {
  previewingContract.value = contract
  highlightCode()
}

// 表格筛选相关
const getColumnFilters = (prop: string) => {
  const values = new Set(tableData.value.map(item => item[prop]))
  return Array.from(values).map(value => ({
    text: value,
    value: value
  }))
}

const filterHandler = (value: any, row: any, column: any) => {
  const property = column.property
  return row[property] === value
}

// 代码高亮函数
const highlightCode = () => {
  nextTick(() => {
    // @ts-ignore
    if (window.Prism) {
      // @ts-ignore
      window.Prism.highlightAll()
    }
  })
}

onMounted(() => {
  handleSearch()
})
</script>

<style lang="scss" scoped>
.rule-management {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: calc(100vh - 40px);

  .operation-bar {
    margin-bottom: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;

    .right {
      display: flex;
      gap: 10px;
    }
  }

  .pagination-container {
    margin-top: 20px;
    display: flex;
    justify-content: flex-end;
  }

  .add-button {
    position: fixed;
    right: 40px;
    bottom: 40px;
    width: 50px;
    height: 50px;
  }
}

.dialog-content {
  display: flex;
  gap: 20px;
  max-height: 70vh;
  overflow-y: auto;

  .form-section {
    flex: 1;
    min-width: 600px;
  }

  .contract-section {
    width: 400px;
    background-color: #f5f7fa;
    padding: 16px;
    border-radius: 4px;

    .contract-header {
      margin-bottom: 16px;

      h3 {
        margin: 0 0 8px;
        font-size: 16px;
        font-weight: 500;
      }

      .contract-info {
        margin: 0;
        color: #606266;
        font-size: 14px;

        span {
          display: block;
          margin-bottom: 4px;
        }
      }
    }

    .source-code {
      background-color: #2d2d2d;
      padding: 16px;
      border-radius: 4px;
      max-height: calc(100vh - 300px);
      overflow-y: auto;

      pre {
        margin: 0;
        code {
          font-family: 'Consolas', 'Monaco', monospace;
          font-size: 14px;
          line-height: 1.5;
        }
      }
    }
  }
}

.function-section {
  margin-bottom: 20px;
  padding: 16px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;

  .function-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;

    h3 {
      margin: 0;
      font-size: 16px;
      font-weight: 500;
    }
  }
}

.param-item {
  margin-bottom: 16px;

  .param-row {
    display: flex;
    gap: 10px;
    align-items: center;
  }
}

.contract-dialog {
  .contract-detail {
    h3 {
      margin: 20px 0 16px;
      font-size: 16px;
      font-weight: 500;
    }

    .contract-info {
      margin-bottom: 24px;
    }

    .contract-source {
      .code-wrapper {
        background-color: #2d2d2d;
        padding: 16px;
        border-radius: 4px;
        max-height: 400px;
        overflow-y: auto;

        pre {
          margin: 0;
          code {
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 14px;
            line-height: 1.5;
          }
        }
      }
    }

    .contract-functions {
      margin-top: 24px;
    }
  }
}

.contract-selector {
  .search-bar {
    margin-bottom: 16px;
  }

  .contract-selector-content {
    display: flex;
    gap: 20px;

    .contract-list {
      flex: 1;
      min-width: 600px;
    }

    .contract-preview {
      width: 500px;
      background-color: #f5f7fa;
      padding: 16px;
      border-radius: 4px;

      .preview-header {
        margin-bottom: 16px;

        h3 {
          margin: 0 0 8px;
          font-size: 16px;
          font-weight: 500;
        }

        .contract-info {
          margin: 0;
          color: #606266;
          font-size: 14px;

          span {
            display: block;
            margin-bottom: 4px;
          }
        }
      }

      .preview-content {
        background-color: #2d2d2d;
        padding: 16px;
        border-radius: 4px;
        height: 500px;
        overflow-y: auto;

        pre {
          margin: 0;
          code {
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 14px;
            line-height: 1.5;
          }
        }
      }
    }
  }

  .pagination {
    margin-top: 16px;
    display: flex;
    justify-content: flex-end;
  }
}
</style> 