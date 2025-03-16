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
      <el-table-column 
        type="index" 
        label="序号" 
        width="80" 
        :index="(index) => (currentPage - 1) * pageSize + index + 1"
      />
      
      <el-table-column 
        prop="contractAddress" 
        label="被监管合约地址" 
        min-width="200" 
        sortable 
        :filters="getColumnFilters('contractAddress')" 
        :filter-method="filterHandler"
      >
        <template #default="{ row }">
          <el-button link type="primary" @click="viewContract(row)">
            {{ row.contractAddress }}
          </el-button>
        </template>
      </el-table-column>

      <el-table-column 
        prop="ruleId" 
        label="监管规则编号" 
        min-width="150" 
        sortable 
        :filters="getColumnFilters('ruleId')" 
        :filter-method="filterHandler" 
      />

      <el-table-column 
        prop="name" 
        label="规则名称" 
        min-width="150" 
        sortable 
        :filters="getColumnFilters('name')" 
        :filter-method="filterHandler" 
      />
      
      <el-table-column 
        prop="regulatorAddress" 
        label="监管账户地址" 
        min-width="200" 
        sortable 
        :filters="getColumnFilters('regulatorAddress')" 
        :filter-method="filterHandler" 
      />
      
      <el-table-column 
        prop="description" 
        label="简介" 
        min-width="200" 
        show-overflow-tooltip 
      />
      
      <el-table-column 
        prop="owner" 
        label="所属用户" 
        min-width="120" 
        sortable 
        :filters="getColumnFilters('owner')" 
        :filter-method="filterHandler" 
      />

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
          <el-scrollbar height="calc(70vh - 100px)">
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
                  :disabled="isEdit"
                  @click="!isEdit && showContractSelector"
                >
                  <template #append>
                    <el-button @click="showContractSelector" :disabled="isEdit">选择合约</el-button>
                  </template>
                </el-input>
              </el-form-item>

              <el-form-item label="监管账户地址" prop="regulatorAddress">
                <div class="regulator-address-container">
                  <el-input
                    v-model="form.regulatorAddress"
                    placeholder="请输入监管账户地址"
                    @focus="showAddressSelector = true"
                  />
                  <!-- 下拉选择区域 -->
                  <div v-show="showAddressSelector" class="address-selector">
                    <div class="selector-header">
                      <span>选择已有监管账户</span>
                      <el-icon class="close-icon" @click="showAddressSelector = false">
                        <Close />
                      </el-icon>
                    </div>
                    <el-scrollbar max-height="200px">
                      <div 
                        v-for="addr in existingRegulatorAddresses" 
                        :key="addr"
                        class="address-item"
                        @click="selectAddress(addr)"
                      >
                        {{ addr }}
                      </div>
                    </el-scrollbar>
                  </div>
                </div>
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
                  <div class="function-name-container">
                    <el-input
                      v-model="func.name"
                      placeholder="请选择或输入函数名称"
                      @focus="showFunctionSelector = true"
                    />
                    <!-- 函数名称下拉选择区域 -->
                    <div v-show="showFunctionSelector" class="function-selector">
                      <div class="selector-header">
                        <span>选择合约函数</span>
                        <el-icon class="close-icon" @click="showFunctionSelector = false">
                          <Close />
                        </el-icon>
                      </div>
                      <el-scrollbar max-height="200px">
                        <div 
                          v-for="name in contractFunctions" 
                          :key="name"
                          class="function-item"
                          @click="selectFunction(funcIndex, name)"
                        >
                          {{ name }}
                        </div>
                      </el-scrollbar>
                    </div>
                  </div>
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
          </el-scrollbar>
        </div>

        <!-- 右侧合约源码 -->
        <div v-if="selectedContract" class="contract-section">
          <div class="contract-header">
            <h3>合约信息</h3>
            <p class="contract-info">
              <span>名称：{{ selectedContractName || '未选择合约' }}</span>
              <span>地址：{{ form.contractAddress || '未选择合约' }}</span>
              <el-button 
                type="primary" 
                size="small"
                @click="loadContractSource"
                :loading="loadingSource"
                :disabled="!form.contractAddress"
              >
                查看源码
              </el-button>
            </p>
          </div>
          <div v-if="showSourceCode" class="source-code">
            <pre><code class="language-solidity">{{ contractSourceCode }}</code></pre>
          </div>
          <div v-else class="empty-source">
            <el-empty description="点击上方按钮查看合约源码" />
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
import { ref, onMounted, nextTick, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search, Plus, Delete, Close } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import { getRuleList, addRule, updateRule, deleteRule, getContractList, getRuleDetail, getContractDetail } from '@/api/rules'
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
const contractFunctions = ref<string[]>([])
const isEditingAddress = ref(false)
const showAddressSelector = ref(false)
const showFunctionSelector = ref(false)

// 表单数据
const form = ref({
  id: '',
  name: '',
  contractAddress: '',
  regulatorAddress: '',
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
  regulatorAddress: [
    { required: true, message: '请输入监管账户地址', trigger: 'blur' },
    { 
      pattern: /^0x[0-9a-fA-F]{40}$/, 
      message: '请输入有效的以太坊地址', 
      trigger: 'blur' 
    }
  ],
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
    const res = await getRuleList({
      page: currentPage.value,
      pageSize: pageSize.value,
      keyword: searchQuery.value
    })
    
    console.log('API Response:', res)
    
    if (res.code === 200) {  // 移除 res.data
      tableData.value = res.data.list
      total.value = res.data.total
      
      // 如果当前页大于最大页数，跳转到最后一页
      const maxPage = Math.ceil(total.value / pageSize.value)
      if (currentPage.value > maxPage && maxPage > 0) {
        currentPage.value = maxPage
        await handleSearch() // 重新加载数据
      }
    } else {
      ElMessage.error(res.message || '获取数据失败')
    }
  } catch (error) {
    console.error('获取数据失败:', error)
    ElMessage.error('获取数据失败')
  } finally {
    loading.value = false
  }
}

const handleReset = async () => {
  searchQuery.value = ''
  currentPage.value = 1
  await handleSearch()
}

const handleSizeChange = async (val: number) => {
  pageSize.value = val
  currentPage.value = 1 // 切换每页条数时重置为第一页
  await handleSearch()
}

const handleCurrentChange = async (val: number) => {
  currentPage.value = val
  await handleSearch()
}

const handleAdd = () => {
  isEdit.value = false
  isEditingAddress.value = false  // 重置编辑状态
  
  // 重置表单数据
  form.value = {
    id: '',
    name: '',
    contractAddress: '',
    regulatorAddress: '',
    description: '',
    owner: storeUser.userInfo?.username || 'super', // 使用当前登录用户名
    functions: [{  // 默认添加一个空函数
      name: '',
      params: []
    }]
  }
  
  // 清空选中的合约
  selectedContract.value = null
  selectedContractName.value = ''
  
  dialogVisible.value = true
}

const handleEdit = async (row: any) => {
  isEdit.value = true
  isEditingAddress.value = false
  dialogVisible.value = true
  
  try {
    // 设置基本表单数据
    form.value = {
      id: row.id,
      name: row.name,
      contractAddress: row.contractAddress,
      regulatorAddress: row.regulatorAddress,
      description: row.description,
      owner: row.owner,
      functions: row.functions || []
    }
    
    // 查找并设置合约信息
    const contract = contracts.value.find(c => c.address === row.contractAddress)
    console.log('Found contract:', contract)
    
    if (contract) {
      selectedContract.value = contract
      selectedContractName.value = `${contract.name} (${contract.address})`
      
      // 更新可用函数列表
      if (contract.abi?.functions) {
        contractFunctions.value = contract.abi.functions.map(f => f.name)
      }
    }
    
    // 重置源码显示状态
    showSourceCode.value = false
    
  } catch (error) {
    console.error('设置表单数据失败:', error)
    ElMessage.error('设置表单数据失败')
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
    
    const res = await deleteRule(row.id)
    if (res.code === 200) {
      ElMessage.success('删除成功')
      
      // 如果当前页只有一条数据，且不是第一页，则跳转到上一页
      if (tableData.value.length === 1 && currentPage.value > 1) {
        currentPage.value--
      }
      
      await handleSearch() // 刷新页面数据
    } else {
      ElMessage.error(res.message || '删除失败')
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败:', error)
      ElMessage.error('删除失败，请重试')
    }
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

// 添加 formRef 定义
const formRef = ref()

// 修改 handleSubmit 函数，在提交时包含 ID
const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    
    const submitData = {
      name: form.value.name,
      contractAddress: form.value.contractAddress,
      regulatorAddress: form.value.regulatorAddress,
      description: form.value.description,
      owner: form.value.owner,
      functions: form.value.functions.map(func => ({
        name: func.name,
        params: func.params.map(param => ({
          name: param.name,
          type: param.type,
          condition: param.condition,
          value: param.value
        }))
      }))
    }

    let res
    if (isEdit.value) {
      // 编辑模式，移除 contractAddress
      delete submitData.contractAddress
      res = await updateRule(Number(form.value.id), submitData)
    } else {
      // 新增模式，包含所有字段
      res = await addRule(submitData)
    }

    if (res.code === 200) {
      ElMessage.success(isEdit.value ? '更新成功' : '添加成功')
      dialogVisible.value = false
      await handleSearch()
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

const selectContract = async (contract: any) => {
  try {
    // 如果选择了不同的合约，清空之前的源码
    if (form.value.contractAddress !== contract.address) {
      showSourceCode.value = false
      contractSourceCode.value = ''
    }
    
    // 设置新的合约信息
    form.value.contractAddress = contract.address
    selectedContractName.value = `${contract.name} (${contract.address})`
    selectedContract.value = contract
    
    // 获取合约源码并解析函数
    const res = await getContractDetail(contract.address)
    if (res.code === 200 && res.data) {
      // 解析源码中的函数名称
      contractFunctions.value = parseFunctionsFromSource(res.data.source_code)
    }
    
    contractSelectorVisible.value = false
  } catch (error) {
    console.error('获取合约详情失败:', error)
    ElMessage.error('获取合约详情失败')
  }
}

// 修改解析函数，只获取函数名
const parseFunctionsFromSource = (sourceCode: string): string[] => {
  const functions: string[] = []
  const lines = sourceCode.split('\n')
  
  for (const line of lines) {
    // 只匹配函数名称
    const match = line.trim().match(/function\s+(\w+)\s*\(/)
    if (match && match[1]) {
      functions.push(match[1])
    }
  }
  
  return functions
}

// 合约预览相关
const previewingContract = ref<any>(null)

const previewContract = async (contract: any) => {
  try {
    // 先设置预览的合约基本信息（不包含源码）
    previewingContract.value = { ...contract, sourceCode: '加载中...' }
    
    // 调用 API 获取最新的合约源码
    if (contract.address) {
      const res = await getContractDetail(contract.address)
      
      if (res.code === 200 && res.data) {
        // 更新合约源码
        previewingContract.value = {
          ...previewingContract.value,
          sourceCode: formatSourceCode(res.data.source_code || '// No source code available')
        }
        
        // 应用代码高亮
        nextTick(() => {
          highlightCode()
        })
      } else {
        previewingContract.value.sourceCode = '// 获取源码失败'
        console.error('获取合约源码失败:', res.message)
      }
    }
  } catch (error) {
    previewingContract.value.sourceCode = '// 获取源码失败'
    console.error('预览合约源码失败:', error)
    ElMessage.error('获取合约源码失败')
  }
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
    if (typeof window.Prism !== 'undefined') {
      try {
        const codeElements = document.querySelectorAll('pre code')
        codeElements.forEach((element) => {
          window.Prism.highlightElement(element)
        })
      } catch (e) {
        console.error('代码高亮失败:', e)
      }
    } else {
      // 如果 Prism 未加载，尝试加载
      loadPrismJS()
    }
  })
}

// 删除原有的 commonRegulatorAddresses 定义，替换为：
const existingRegulatorAddresses = computed(() => {
  // 从表格数据中提取不重复的监管账户地址
  return Array.from(new Set(tableData.value.map(item => item.regulatorAddress)))
    .filter(addr => addr) // 过滤掉空值
})

// 添加编辑地址的处理方法
const handleEditAddress = () => {
  isEditingAddress.value = true
}

const handleAddressEditComplete = () => {
  isEditingAddress.value = false
  // 验证地址格式
  if (form.value.regulatorAddress && !/^0x[0-9a-fA-F]{40}$/.test(form.value.regulatorAddress)) {
    ElMessage.warning('请输入有效的以太坊地址')
    form.value.regulatorAddress = ''
  }
}

const selectAddress = (address: string) => {
  form.value.regulatorAddress = address
  showAddressSelector.value = false
}

// 新增的合约源码相关
const loadingSource = ref(false)
const showSourceCode = ref(false)
const contractSourceCode = ref('')

const loadContractSource = async () => {
  if (!form.value.contractAddress) {
    ElMessage.warning('未找到合约地址')
    return
  }

  try {
    loadingSource.value = true
    showSourceCode.value = false
    
    const res = await getContractDetail(form.value.contractAddress)
    
    if (res.code === 200) {
      // 格式化源码
      const sourceCode = res.data.source_code || '// No source code available'
      contractSourceCode.value = formatSourceCode(sourceCode)
      showSourceCode.value = true
      
      nextTick(() => {
        if (typeof window.Prism === 'undefined') {
          loadPrismJS()
        } else {
          highlightCode()
        }
      })
    } else {
      ElMessage.error('获取合约源码失败')
    }
  } catch (error) {
    console.error('获取合约源码失败:', error)
    ElMessage.error('获取合约源码失败')
  } finally {
    loadingSource.value = false
  }
}

// 添加源码格式化函数
const formatSourceCode = (sourceCode: string): string => {
  // 1. 移除开头和结尾的空白字符
  let formattedCode = sourceCode.trim()
  
  // 2. 按行分割
  const lines = formattedCode.split('\n')
  
  // 3. 处理每一行
  formattedCode = lines
    .map(line => {
      // 移除每行开头的所有空白字符
      const trimmedLine = line.trim()
      
      if (!trimmedLine) {
        // 空行直接返回
        return ''
      }
      
      // 根据代码层级添加适当的缩进
      if (trimmedLine.includes('contract') || trimmedLine.includes('pragma') || trimmedLine.includes('SPDX')) {
        // 合约声明、pragma 和 license 声明不缩进
        return trimmedLine
      } else if (trimmedLine.startsWith('function')) {
        // 函数声明缩进 4 个空格
        return '    ' + trimmedLine
      } else if (trimmedLine.startsWith('//')) {
        // 注释缩进 4 个空格
        return '    ' + trimmedLine
      } else if (trimmedLine.includes('{') || trimmedLine.includes('}')) {
        // 大括号缩进 4 个空格
        return '    ' + trimmedLine
      } else {
        // 其他内容缩进 8 个空格
        return '        ' + trimmedLine
      }
    })
    .join('\n')
  
  return formattedCode
}

// 添加加载 Prism 的函数
const loadPrismJS = () => {
  // 检查是否已经加载
  if (document.getElementById('prism-css') || document.getElementById('prism-js')) {
    return
  }
  
  // 加载 Prism CSS
  const link = document.createElement('link')
  link.id = 'prism-css'
  link.rel = 'stylesheet'
  link.href = 'https://cdn.jsdelivr.net/npm/prismjs@1.29.0/themes/prism-tomorrow.min.css'
  document.head.appendChild(link)
  
  // 加载 Prism JS
  const script = document.createElement('script')
  script.id = 'prism-js'
  script.src = 'https://cdn.jsdelivr.net/npm/prismjs@1.29.0/components/prism-core.min.js'
  script.onload = () => {
    // 加载 Solidity 语言支持
    const solidityScript = document.createElement('script')
    solidityScript.src = 'https://cdn.jsdelivr.net/npm/prismjs@1.29.0/components/prism-solidity.min.js'
    solidityScript.onload = () => {
      highlightCode()
    }
    document.head.appendChild(solidityScript)
  }
  document.head.appendChild(script)
}

// 添加类型声明
declare global {
  interface Window {
    Prism: any
  }
}

// 添加选择函数的方法
const selectFunction = (funcIndex: number, name: string) => {
  form.value.functions[funcIndex].name = name
  showFunctionSelector.value = false
}

onMounted(async () => {
  handleSearch()
  // 获取合约列表
  try {
    const res = await getContractList()
    console.log('Contract list response:', res) // 添加日志
    if (res.code === 200) {
      contracts.value = res.data.list
      filteredContracts.value = res.data.list
      
      // 更新可用函数列表
      if (selectedContract.value) {
        contractFunctions.value = selectedContract.value.abi?.functions?.map(f => f.name) || []
      }
    } else {
      ElMessage.error(res.message || '获取合约列表失败')
    }
  } catch (error) {
    console.error('获取合约列表失败:', error)
    ElMessage.error('获取合约列表失败')
  }

  // 添加点击外部关闭下拉框的处理
  document.addEventListener('click', (e) => {
    const target = e.target as HTMLElement
    if (!target.closest('.regulator-address-container')) {
      showAddressSelector.value = false
    }
  })

  // 添加点击外部关闭函数选择器的处理
  document.addEventListener('click', (e) => {
    const target = e.target as HTMLElement
    if (!target.closest('.function-name-container')) {
      showFunctionSelector.value = false
    }
  })
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
  height: 70vh;  // 固定高度
  
  .form-section {
    flex: 1;
    min-width: 600px;
    overflow: hidden;  // 防止溢出
    
    .rule-form {
      padding: 20px;
    }
  }

  .contract-section {
    width: 400px;
    background-color: #f5f7fa;
    border-radius: 4px;
    overflow: hidden;  // 防止溢出
    display: flex;
    flex-direction: column;

    .contract-header {
      padding: 16px;
      background-color: #fff;
      border-bottom: 1px solid #dcdfe6;
      
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
          margin-bottom: 8px;
        }
      }
    }

    .source-code {
      padding: 16px;
      background-color: #2d2d2d;
      flex: 1;
      overflow-y: auto;
      
      pre {
        margin: 0;
        
        code {
          font-family: 'Consolas', 'Monaco', monospace;
          font-size: 14px;
          line-height: 1.5;
          white-space: pre-wrap;
          tab-size: 4;
          display: block;
          color: #f8f8f2;  // 设置默认文本颜色
          background: none;  // 移除默认背景色
        }
      }
    }
    
    .empty-source {
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: center;
      background-color: #f5f7fa;
      padding: 20px;
    }
  }
}

.function-section {
  margin-bottom: 20px;
  padding: 16px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  background-color: #fff;  // 添加背景色
}

.param-item {
  margin-bottom: 16px;

  .param-row {
    display: flex;
    flex-wrap: wrap;  // 添加换行
    gap: 10px;
    align-items: center;

    // 设置每个输入框的宽度
    .el-input,
    .el-select {
      flex: 1;
      min-width: 120px;  // 设置最小宽度
      max-width: 200px;  // 设置最大宽度，防止拉伸过长
    }

    // 删除按钮样式
    .el-button {
      flex-shrink: 0;  // 防止按钮被压缩
    }
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

.regulator-address-container {
  position: relative;
  width: 100%;

  .address-selector {
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    margin-top: 4px;
    background: white;
    border: 1px solid #dcdfe6;
    border-radius: 4px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
    z-index: 100;

    .selector-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 8px 12px;
      border-bottom: 1px solid #ebeef5;
      
      .close-icon {
        cursor: pointer;
        color: #909399;
        &:hover {
          color: #409EFF;
        }
      }
    }

    .address-item {
      padding: 8px 12px;
      cursor: pointer;
      transition: background-color 0.3s;
      
      &:hover {
        background-color: #f5f7fa;
        color: #409EFF;
      }
    }
  }
}

.function-name-container {
  position: relative;
  width: 100%;

  .function-selector {
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    margin-top: 4px;
    background: white;
    border: 1px solid #dcdfe6;
    border-radius: 4px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
    z-index: 100;

    .selector-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 8px 12px;
      border-bottom: 1px solid #ebeef5;
      
      .close-icon {
        cursor: pointer;
        color: #909399;
        &:hover {
          color: #409EFF;
        }
      }
    }

    .function-item {
      padding: 8px 12px;
      cursor: pointer;
      transition: background-color 0.3s;
      
      &:hover {
        background-color: #f5f7fa;
        color: #409EFF;
      }
    }
  }
}
</style> 