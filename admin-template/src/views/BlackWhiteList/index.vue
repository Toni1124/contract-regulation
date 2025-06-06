<template>
  <div class="black-white-list">
    <!-- 搜索和添加按钮区域 -->
    <div class="operation-bar">
      <el-input
        v-model="searchQuery"
        placeholder="请输入账户地址"
        style="width: 300px"
        @input="handleSearch"
      />
      <el-button type="primary" @click="handleAdd">添加</el-button>
    </div>

    <!-- 表格区域 -->
    <el-table 
      :data="tableData" 
      border 
      style="width: 100%"
      :fit="true"
    >
      <el-table-column 
        prop="address" 
        label="账户地址" 
        min-width="280"
        :filters="addressFilters"
        :filter-method="filterAddress"
      />
      <el-table-column 
        prop="operateTime" 
        label="操作时间" 
        min-width="180"
        sortable
      >
        <template #default="{ row }">
          {{ formatDate(row.operateTime) }}
        </template>
      </el-table-column>
      <el-table-column 
        prop="operator" 
        label="操作人" 
        min-width="120"
        :filters="operatorFilters"
        :filter-method="filterHandler"
      />
      <el-table-column 
        prop="type" 
        label="类型" 
        min-width="100"
        :filters="[
          { text: '白名单', value: 1 },
          { text: '黑名单', value: 2 }
        ]"
        :filter-method="filterType"
      >
        <template #default="{ row }">
          <el-tag :type="row.type === 1 ? 'success' : 'danger'">
            {{ row.type === 1 ? '白名单' : '黑名单' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column 
        prop="organization" 
        label="发布机构" 
        min-width="150"
        :filters="organizationFilters"
        :filter-method="filterHandler"
      />
      <el-table-column 
        prop="region" 
        label="使用范围" 
        min-width="120"
        :filters="defaultRegions"
        :filter-method="filterHandler"
      >
        <template #default="{ row }">
          <el-tag :type="getRegionTagType(row.region)">
            {{ row.region }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" min-width="200" fixed="right">
        <template #default="{ row }">
          <el-button type="primary" size="small" @click="handleEdit(row)">编辑</el-button>
          <el-button type="danger" size="small" @click="handleDelete(row)">删除</el-button>
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

    <!-- 添加/编辑弹窗 -->
    <el-dialog
      :title="dialogTitle"
      v-model="dialogVisible"
      width="500px"
    >
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="账户地址" prop="address">
          <el-input v-model="form.address" placeholder="请输入账户地址" />
        </el-form-item>
        <el-form-item label="操作人" prop="operator">
          <el-select
            v-model="form.operator"
            filterable
            allow-create
            default-first-option
            placeholder="请选择或输入操作人"
            style="width: 100%"
          >
            <el-option
              v-for="item in defaultOperators"
              :key="item.value"
              :label="item.text"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="类型" prop="type">
          <el-select v-model="form.type" placeholder="请选择类型" style="width: 100%">
            <el-option label="白名单" :value="1" />
            <el-option label="黑名单" :value="2" />
          </el-select>
        </el-form-item>
        <el-form-item label="发布机构" prop="organization">
          <el-select
            v-model="form.organization"
            filterable
            allow-create
            default-first-option
            placeholder="请选择或输入发布机构"
            style="width: 100%"
          >
            <el-option
              v-for="item in defaultOrganizations"
              :key="item.value"
              :label="item.text"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="使用范围" prop="region">
          <el-select
            v-model="form.region"
            filterable
            allow-create
            default-first-option
            placeholder="请选择或输入使用范围"
            style="width: 100%"
          >
            <el-option
              v-for="item in defaultRegions"
              :key="item.value"
              :label="item.text"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import type { FormInstance } from 'element-plus'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getList, addItem, updateItem, deleteItem } from '@/api/blackWhiteList'
import { getSystemConfig } from '@/api/system'

interface FormData {
  id?: number
  address: string
  operator: string
  type: number
  organization: string
  region: string
  operateTime?: string
}

interface SystemOption {
  id: number
  name: string
}

const searchQuery = ref('')
const tableData = ref([])
const dialogVisible = ref(false)
const dialogTitle = ref('')
const formRef = ref<FormInstance>()

// 默认选项
const defaultRegions = [
  { text: '香港', value: '香港' },
  { text: '中国大陆', value: '中国大陆' },
  { text: '不限', value: '不限' },
  { text: '澳门', value: '澳门' },
  { text: '深圳', value: '深圳' }
]

const defaultOperators = [
  { text: 'Admin', value: 'Admin' },
  { text: 'Operator', value: 'Operator' }
]

const defaultOrganizations = [
  { text: '中国人民银行', value: '中国人民银行' },
  { text: '中央网信办', value: '中央网信办' },
  { text: '香港金管局', value: '香港金管局' }
]

// 表单数据
const form = ref<FormData>({
  address: '',
  operator: '',
  type: 1,
  organization: '',
  region: '不限' // 默认值
})

// 表单验证规则
const rules = {
  address: [
    { required: true, message: '请输入账户地址', trigger: 'blur' },
    { pattern: /^0x[0-9a-fA-F]{40}$/, message: '请输入正确的以太坊账户地址', trigger: 'blur' }
  ],
  operator: [
    { required: true, message: '请选择操作人', trigger: 'change' }
  ],
  type: [
    { required: true, message: '请选择类型', trigger: 'change' },
    { type: 'number', min: 1, max: 2, message: '类型只能是1或2', trigger: 'change' }
  ],
  organization: [
    { required: true, message: '请选择发布机构', trigger: 'change' }
  ],
  region: [
    { required: true, message: '请选择使用范围', trigger: 'change' }
  ]
}

// 系统配置数据
const regionOptions = ref<SystemOption[]>([])
const operatorOptions = ref<SystemOption[]>([])
const organizationOptions = ref<SystemOption[]>([])

// 获取系统配置
const fetchSystemConfig = async () => {
  try {
    const res = await getSystemConfig()
    if (res.code === 200) {
      regionOptions.value = res.data.regions
      operatorOptions.value = res.data.operators
      organizationOptions.value = res.data.organizations
    }
  } catch (error) {
    //console.error('获取系统配置失败:', error)
    //ElMessage.error('获取系统配置失败')
  }
}

// 表格筛选器选项
const regionFilters = computed(() => 
  regionOptions.value.map(item => ({
    text: item.name,
    value: item.id
  }))
)

// 获取区域名称
const getRegionName = (regionId: number) => {
  const region = regionOptions.value.find(item => item.id === regionId)
  return region ? region.name : ''
}

// 获取区域标签类型
const getRegionTagType = (region: string) => {
  const types: Record<string, string> = {
    '香港': 'warning',
    '中国大陆': 'success',
    '不限': 'info',
    '澳门': 'danger',
    '深圳': 'primary'
  }
  return types[region] || 'info'
}

// 分页相关的响应式变量
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

// 日期格式化函数
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

// 获取列表数据
const fetchData = async () => {
  try {
    const params = {
      page: currentPage.value,
      pageSize: pageSize.value,
      keyword: searchQuery.value
    }
    const res = await getList(params)
    console.log("Received data:", res.data)  // 打印接收到的数据
    if (res.code === 200) {
      // 对数据按操作时间降序排序
      const sortedData = res.data.list.sort((a, b) => 
        new Date(b.operateTime).getTime() - new Date(a.operateTime).getTime()
      )
      tableData.value = sortedData
      total.value = res.data.total
    } else {
      ElMessage.error(res.message)
    }
  } catch (error) {
    console.error('获取数据失败:', error)
    ElMessage.error('获取数据失败')
  }
}

// 处理每页条数变化
const handleSizeChange = (val: number) => {
  pageSize.value = val
  fetchData()
}

// 处理页码变化
const handleCurrentChange = (val: number) => {
  currentPage.value = val
  fetchData()
}

// 搜索时重置页码
const handleSearch = () => {
  currentPage.value = 1
  fetchData()
}

// 添加
const handleAdd = () => {
  dialogTitle.value = '添加名单'
  form.value = {
    address: '',
    operator: '',
    type: 1,
    organization: '',
    region: '不限'
  }
  dialogVisible.value = true
}

// 编辑
const handleEdit = (row: FormData) => {
  dialogTitle.value = '编辑名单'
  // 确保深拷贝数据
  form.value = {
    id: row.id,
    address: row.address,
    operator: row.operator,  // 确保这个值在 defaultOperators 中存在
    type: row.type,
    organization: row.organization,
    region: row.region
  }
  
  // 如果操作人不在默认选项中，添加到选项列表
  if (!defaultOperators.some(op => op.value === row.operator)) {
    defaultOperators.push({
      text: row.operator,
      value: row.operator
    })
  }
  
  dialogVisible.value = true
}

// 删除
const handleDelete = async (row: FormData) => {
  try {
    await ElMessageBox.confirm(
      '确认删除该记录吗？此操作将不可恢复',
      '删除确认',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    const res = await deleteItem(row.id!)
    if (res.code === 200) {
      ElMessage.success('删除成功')
      fetchData() // 重新获取数据
    } else {
      ElMessage.error(res.message)
    }
  } catch (error) {
    console.error(error)
    ElMessage.error('删除失败')
  }
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    
    // 检查地址是否重复
    const isDuplicate = tableData.value.some(item => 
      // 排除当前编辑的记录
      item.id !== form.value.id && 
      item.address.toLowerCase() === form.value.address.toLowerCase()
    )

    if (isDuplicate) {
      ElMessage.error('该地址已存在，请勿重复添加')
      return
    }

    // 构建要发送的数据对象
    const submitData = {
      address: form.value.address,
      operator: form.value.operator.trim(),
      type: form.value.type,
      organization: form.value.organization,
      region: form.value.region
    }

    // 打印要发送的数据，方便调试
    console.log('Submitting data:', {
      id: form.value.id,
      data: submitData
    })

    const res = form.value.id 
      ? await updateItem(form.value.id, submitData)
      : await addItem(submitData)

    console.log('Response:', res)

    if (res.code === 200) {
      ElMessage.success(form.value.id ? '更新成功' : '添加成功')
      dialogVisible.value = false
      await fetchData()
    } else {
      if ('errors' in res) {
        const errorMsg = Object.values(res.errors).flat().join(', ')
        ElMessage.error(errorMsg || res.message)
      } else {
        ElMessage.error(res.message || '操作失败')
      }
    }
  } catch (error) {
    console.error('操作失败:', error)
    if (error instanceof Error) {
      ElMessage.error(`操作失败: ${error.message}`)
    } else {
      ElMessage.error('操作失败，请重试')
    }
  }
}

// 生成筛选器选项
const addressFilters = computed(() => {
  const addresses = Array.from(new Set(tableData.value.map(item => item.address)))
  return addresses.map(address => ({ text: address, value: address }))
})

const operatorFilters = computed(() => {
  const operators = Array.from(new Set(tableData.value.map(item => item.operator)))
  return operators.map(operator => ({ text: operator, value: operator }))
})

const organizationFilters = computed(() => {
  const organizations = Array.from(new Set(tableData.value.map(item => item.organization)))
  return organizations.map(org => ({ text: org, value: org }))
})

// 筛选方法
const filterHandler = (value: string, row: any, column: any) => {
  const property = column.property
  return row[property] === value
}

const filterAddress = (value: string, row: any) => {
  return row.address.toLowerCase().includes(value.toLowerCase())
}

const filterType = (value: number, row: any) => {
  return row.type === value
}

// 页面初始化
onMounted(async () => {
  await fetchSystemConfig() // 先获取系统配置
  fetchData()              // 再获取表格数据
})
</script>

<style scoped>
.black-white-list {
  padding: 20px;
  background-color: #f5f7fa;  /* 设置背景色 */
  min-height: calc(100vh - 40px);  /* 确保最小高度填充整个视图 */
}

/* 可选：设置表格背景色 */
:deep(.el-table) {
  --el-table-bg-color: #ffffff;
  --el-table-tr-bg-color: #ffffff;
  width: 100% !important;  /* 强制表格宽度100% */
}

.operation-bar {
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

/* 添加筛选器样式 */
:deep(.el-table-filter) {
  background-color: #ffffff;
}

:deep(.el-table-filter__list) {
  max-height: 300px;
  overflow-y: auto;
}
</style> 