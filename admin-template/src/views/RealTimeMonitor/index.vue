<template>
  <div class="realtime-monitor">
    <!-- 移除滚动指示器，只保留搜索框 -->
    <div class="operation-bar">
      <el-input
        v-model="searchQuery"
        placeholder="请输入地址或交易哈希"
        style="width: 300px"
        @input="handleSearch"
      />
    </div>

    <!-- 表格容器 -->
    <div class="table-container">
      <el-table 
        ref="tableRef"
        :data="currentPageData" 
        border 
        style="width: max-content; min-width: 100%"
        v-loading="isLoading"
      >
        <!-- 固定前三列 -->
        <el-table-column 
          prop="request_time" 
          label="时间戳" 
          width="180"
          fixed="left"
          sortable
        >
          <template #default="{ row }">
            {{ formatDate(row.request_time) }}
          </template>
        </el-table-column>
        <el-table-column 
          prop="block_number" 
          label="区块号" 
          width="120"
          fixed="left"
          sortable
        />
        <el-table-column 
          prop="transaction_index" 
          label="交易索引" 
          width="100"
          fixed="left"
        />
        <el-table-column 
          prop="from_address" 
          label="发送方地址" 
          width="280"
          :filters="addressFilters"
          :filter-method="filterAddress"
        />
        <el-table-column 
          prop="to_address" 
          label="接收方地址" 
          width="280"
          :filters="addressFilters"
          :filter-method="filterAddress"
        />
        <el-table-column 
          prop="value" 
          label="交易值" 
          width="120"
        />
        <el-table-column 
          prop="gas" 
          label="Gas" 
          width="100"
        />
        <el-table-column 
          prop="gas_price" 
          label="Gas价格" 
          width="120"
        />
        <el-table-column 
          prop="nonce" 
          label="Nonce" 
          width="100"
        />
        <el-table-column 
          prop="block_hash" 
          label="区块哈希" 
          width="180"
        />
        <el-table-column 
          prop="input" 
          label="输入数据" 
          width="200"
          show-overflow-tooltip
        />
        <el-table-column 
          prop="hash" 
          label="交易哈希" 
          width="180"
        />
        <el-table-column 
          prop="function_signature" 
          label="函数签名" 
          width="150"
        />
        <el-table-column 
          prop="function_name" 
          label="函数名" 
          width="150"
        />
        <el-table-column 
          prop="decoded_parameters" 
          label="解码参数" 
          width="200"
          show-overflow-tooltip
        >
          <template #default="{ row }">
            {{ JSON.stringify(row.decoded_parameters) }}
          </template>
        </el-table-column>
        <el-table-column 
          prop="rules_check_passed" 
          label="规则检查" 
          width="100"
        >
          <template #default="{ row }">
            <el-tag :type="row.rules_check_passed ? 'success' : 'danger'">
              {{ row.rules_check_passed ? '通过' : '未通过' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column 
          prop="rules_check_message" 
          label="检查消息" 
          width="200"
          show-overflow-tooltip
        />
      </el-table>
    </div>

    <!-- 分页器 -->
    <div class="pagination-container">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        :total="tableData.length"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>

    <!-- 加载状态提示 -->
    <div v-if="isLoading" class="loading-tip">
      正在加载最新数据...
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { getInitialData, getUpdates, type TransactionData } from '@/api/realtime'

const searchQuery = ref('')
const tableData = ref<TransactionData[]>([])
const isLoading = ref(false)
const lastTimestamp = ref('')
const pollingTimer = ref<number | null>(null)
const currentPage = ref(1)
const pageSize = ref(20)
const isUpdating = ref(false)

// 添加表格引用
const tableRef = ref()

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

// 修改获取初始数据的函数
const fetchInitialData = async () => {
  try {
    isLoading.value = true
    const res = await getInitialData()
    if (res.code === 200 && res.data && Array.isArray(res.data)) {
      const requestTime = new Date().toISOString()
      tableData.value = res.data.reverse().map(item => ({
        ...item,
        request_time: requestTime
      }))
      
      if (tableData.value.length > 0) {
        lastTimestamp.value = tableData.value[0].block_timestamp
      }
    }
  } catch (error) {
    console.error('Failed to fetch initial data:', error)
  } finally {
    isLoading.value = false
  }
}

// 计算当前页数据
const currentPageData = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return tableData.value.slice(start, end)
})

// 分页处理函数
const handleSizeChange = (val: number) => {
  pageSize.value = val
  currentPage.value = 1
}

const handleCurrentChange = (val: number) => {
  currentPage.value = val
}

// 修改轮询相关的代码
const startPolling = () => {
  console.log('Starting polling')
  stopPolling() // 确保先清除之前的定时器
  // 不要立即设置 interval，而是先执行一次更新
  fetchUpdates()
}

// 添加一个新的函数来设置定时器
const setupInterval = () => {
  if (pollingTimer.value) return; // 如果已经有定时器，不要重复设置
  console.log('Setting up polling interval')
  pollingTimer.value = window.setInterval(fetchUpdates, 5000)
}

// 修改获取更新数据的函数
const fetchUpdates = async () => {
  if (!lastTimestamp.value || isLoading.value || isUpdating.value) {
    return;
  }

  try {
    isUpdating.value = true
    const res = await getUpdates(lastTimestamp.value)
    
    if (res.code === 200 && res.data && Array.isArray(res.data)) {
      if (res.data.length > 0) {
        const requestTime = new Date().toISOString()
        const newRecords = res.data.reverse().map(item => ({
          ...item,
          request_time: requestTime
        }))
        
        tableData.value = [...newRecords, ...tableData.value].slice(0, 1000)
        lastTimestamp.value = tableData.value[0].block_timestamp
        
        ElMessage({
          message: '数据已更新',
          type: 'success',
          duration: 2000,
          customClass: 'update-success-message'
        })
      }
    }
  } catch (error) {
    console.error('Update failed:', error)
  } finally {
    isUpdating.value = false
    // 确保在第一次更新完成后设置定时器
    if (!pollingTimer.value) {
      setupInterval()
    }
  }
}

// 停止轮询
const stopPolling = () => {
  if (pollingTimer.value) {
    clearInterval(pollingTimer.value)
    pollingTimer.value = null
  }
}

// 搜索处理
const handleSearch = () => {
  // 实现搜索逻辑
  console.log('Search query:', searchQuery.value)
}

// 地址筛选器
const addressFilters = computed(() => {
  const addresses = new Set<string>()
  tableData.value.forEach(item => {
    if (item.from_address) addresses.add(item.from_address)
    if (item.to_address) addresses.add(item.to_address)
  })
  return Array.from(addresses).map(address => ({
    text: address,
    value: address
  }))
})

// 地址筛选方法
const filterAddress = (value: string, row: TransactionData) => {
  return row.from_address === value || row.to_address === value
}

// 修改页面初始化
onMounted(async () => {
  await fetchInitialData()
  if (tableData.value.length > 0) {
    // 等待5秒后开始第一次轮询
    setTimeout(startPolling, 5000)
  }
})

// 确保在组件卸载时清理定时器
onUnmounted(() => {
  stopPolling()
})
</script>

<style scoped>
.realtime-monitor {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: calc(100vh - 40px);
  width: 100%;
}

.table-container {
  width: 100%;
  overflow-x: auto;
  position: relative;
}

/* 优化表格样式 */
:deep(.el-table) {
  --el-table-bg-color: #ffffff;
  --el-table-tr-bg-color: #ffffff;
}

/* 美化滚动条 */
.table-container::-webkit-scrollbar {
  height: 8px;
}

.table-container::-webkit-scrollbar-thumb {
  background: #909399;
  border-radius: 4px;
}

.table-container::-webkit-scrollbar-track {
  background: #E4E7ED;
  border-radius: 4px;
}

/* 更新提示样式 */
:deep(.update-success-message) {
  background-color: #67C23A !important;
  color: white !important;
  border-radius: 4px;
  padding: 8px 16px;
}

.operation-bar {
  margin-bottom: 20px;
  display: flex;
  align-items: center;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

/* 确保表格在小屏幕上也能正常显示 */
@media screen and (max-width: 1400px) {
  .table-container {
    margin: 0 -20px;
    padding: 0 20px;
    width: calc(100% + 40px);
  }
}

.loading-tip {
  margin-top: 20px;
  text-align: center;
  color: #909399;
}
</style> 