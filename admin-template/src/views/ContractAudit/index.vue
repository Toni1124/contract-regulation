// 合约审核页面组件 
<template>
  <div class="contract-audit">
    <!-- 搜索和操作区域 -->
    <div class="operation-bar">
      <el-button type="primary" @click="handleSubmit">提交审核</el-button>
    </div>

    <!-- 主要内容区域：左侧代码编辑器，右侧表单 -->
    <div class="main-content">
      <!-- 左侧代码编辑器(临时使用el-input) -->
      <div class="editor-section">
        <div class="section-header">
          <span>合约代码</span>
          <div class="editor-tools">
            <el-select v-model="editorLanguage" size="small" style="width: 120px">
              <el-option label="Solidity" value="solidity" />
              <el-option label="Vyper" value="python" />
            </el-select>
          </div>
        </div>
        <el-input
          v-model="formData.sourceCode"
          type="textarea"
          :rows="20"
          placeholder="请输入合约代码"
        />
      </div>

      <!-- 右侧表单 -->
      <div class="form-section">
        <el-form ref="formRef" :model="formData" :rules="rules" label-width="100px">
          <el-form-item label="合约地址" prop="address">
            <el-input v-model="formData.address" placeholder="请输入已部署的合约地址">
              <template #append>
                <el-button @click="verifyContract">验证</el-button>
              </template>
            </el-input>
          </el-form-item>
          
          <el-form-item label="交易哈希" prop="txHash">
            <el-input v-model="formData.txHash" placeholder="部署合约的交易哈希">
              <template #append>
                <el-button @click="fetchTxInfo">获取</el-button>
              </template>
            </el-input>
          </el-form-item>

          <el-form-item label="合约名称" prop="name">
            <el-input v-model="formData.name" placeholder="请输入合约名称" />
          </el-form-item>

          <el-form-item label="合约版本" prop="version">
            <el-select v-model="formData.version" style="width: 100%">
              <el-option label="0.8.0" value="0.8.0" />
              <el-option label="0.8.17" value="0.8.17" />
              <el-option label="0.8.20" value="0.8.20" />
            </el-select>
          </el-form-item>

          <el-form-item label="优化级别" prop="optimization">
            <el-radio-group v-model="formData.optimization">
              <el-radio :label="true">启用</el-radio>
              <el-radio :label="false">禁用</el-radio>
            </el-radio-group>
          </el-form-item>

          <el-form-item label="合约描述" prop="description">
            <el-input 
              v-model="formData.description" 
              type="textarea" 
              :rows="4"
              placeholder="请输入合约功能描述"
            />
          </el-form-item>
        </el-form>

        <!-- 验证结果展示 -->
        <div v-if="verificationResult" class="verification-result">
          <el-alert
            :title="verificationResult.success ? '验证成功' : '验证失败'"
            :type="verificationResult.success ? 'success' : 'error'"
            :description="verificationResult.message"
            show-icon
          />
        </div>
      </div>
    </div>

    <!-- 审核记录表格 -->
    <div class="table-section">
      <div class="section-header">
        <span>审核记录</span>
      </div>
      
      <!-- 表格工具栏 -->
      <div class="table-toolbar">
        <div class="left">
          <el-input
            v-model="searchQuery"
            placeholder="搜索合约地址/名称"
            style="width: 300px"
            clearable
            @input="handleSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
          <el-select 
            v-model="statusFilter" 
            placeholder="审核状态" 
            style="width: 120px" 
            clearable 
            @change="handleSearch"
          >
            <el-option label="全部" value="" />
            <el-option label="待审核" :value="0" />
            <el-option label="已通过" :value="1" />
            <el-option label="已拒绝" :value="2" />
          </el-select>
        </div>
      </div>

      <!-- 表格 -->
      <el-table 
        :data="tableData" 
        border 
        style="width: 100%"
        v-loading="tableLoading"
      >
        <el-table-column prop="address" label="合约地址" min-width="280">
          <template #default="{ row }">
            <el-tooltip :content="row.address" placement="top" :show-after="500">
              <span class="address-text">{{ row.address }}</span>
            </el-tooltip>
          </template>
        </el-table-column>
        <el-table-column prop="name" label="合约名称" min-width="180" sortable />
        <el-table-column prop="submitTime" label="提交时间" min-width="180" sortable>
          <template #default="{ row }">
            {{ formatDate(row.submitTime) }}
          </template>
        </el-table-column>
        <el-table-column 
          prop="status" 
          label="审核状态" 
          min-width="100"
          :filters="[
            { text: '待审核', value: '0' },
            { text: '已通过', value: '1' },
            { text: '已拒绝', value: '2' }
          ]"
          :filter-method="filterStatus"
        >
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="comment" label="审核意见" min-width="200" show-overflow-tooltip />
        <el-table-column label="操作" width="120" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" @click="handleView(row)">查看详情</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </div>

    <!-- 审核结果弹窗 -->
    <el-dialog
      v-model="auditDialogVisible"
      :title="getDialogTitle(auditResult.status)"
      width="60%"
      :close-on-click-modal="false"
    >
      <div class="audit-result">
        <!-- 基本信息 -->
        <div class="info-section">
          <el-descriptions :column="2" border>
            <el-descriptions-item label="合约地址">{{ auditResult.address }}</el-descriptions-item>
            <el-descriptions-item label="合约名称">{{ auditResult.name }}</el-descriptions-item>
            <el-descriptions-item label="提交时间">{{ formatDate(auditResult.submitTime) }}</el-descriptions-item>
            <el-descriptions-item label="审核状态">
              <el-tag :type="getStatusType(auditResult.status)">
                {{ getStatusText(auditResult.status) }}
              </el-tag>
            </el-descriptions-item>
          </el-descriptions>
        </div>

        <!-- 审核中状态 -->
        <div v-if="auditResult.status === 0" class="auditing-section">
          <el-result
            title="合约审核中"
            sub-title="请耐心等待审核完成"
          >
            <template #extra>
              <el-progress :percentage="50" status="warning" />
            </template>
          </el-result>
        </div>

        <!-- 审核通过状态 -->
        <div v-else-if="auditResult.status === 1" class="success-section">
          <el-result
            icon="success"
            title="审核通过"
            sub-title="您的合约代码符合安全标准"
          />
        </div>

        <!-- 审核未通过状态 - 保持原有的详细风险展示 -->
        <div v-else-if="auditResult.status === 2 && auditResult.details" class="result-section">
          <h3>审核详情</h3>
          <!-- 安全检查结果 -->
          <div v-if="auditResult.details.securityChecks?.length" class="security-checks">
            <div v-for="(check, index) in auditResult.details.securityChecks" :key="index" class="check-item">
              <el-alert
                :title="check.title"
                :type="check.severity"
                :description="check.description"
                show-icon
              >
                <template #default>
                  <div class="code-location" v-if="check.location">
                    <p>位置：第 {{ check.location.line }} 行</p>
                    <pre><code>{{ check.location.code }}</code></pre>
                  </div>
                </template>
              </el-alert>
            </div>
          </div>

          <!-- 相关监管规定 -->
          <div v-if="auditResult.details.regulations?.length" class="regulations">
            <h4>相关监管规定</h4>
            <el-card class="regulation-card">
              <template #header>
                <div class="card-header">
                  <span>法规依据</span>
                </div>
              </template>
              <div v-for="(reg, index) in auditResult.details.regulations" :key="index" class="regulation-item">
                <h5>{{ reg.title }}</h5>
                <p class="regulation-content">{{ reg.content }}</p>
                <p class="regulation-violation">违规情况：{{ reg.violation }}</p>
              </div>
            </el-card>
          </div>

          <!-- 代码质量建议 -->
          <div v-if="auditResult.details.codeQuality?.length" class="code-quality">
            <h4>代码质量建议</h4>
            <el-timeline>
              <el-timeline-item
                v-for="(item, index) in auditResult.details.codeQuality"
                :key="index"
                :type="item.type"
                :color="getQualityColor(item.type)"
              >
                <h4>{{ item.title }}</h4>
                <p>{{ item.suggestion }}</p>
              </el-timeline-item>
            </el-timeline>
          </div>

          <!-- Gas 优化建议 -->
          <div v-if="auditResult.details.gasOptimization?.length" class="gas-optimization">
            <h4>Gas 优化建议</h4>
            <el-collapse>
              <el-collapse-item
                v-for="(item, index) in auditResult.details.gasOptimization"
                :key="index"
                :title="item.title"
              >
                <p>{{ item.description }}</p>
                <div class="code-comparison" v-if="item.example">
                  <div class="before">
                    <h5>优化前</h5>
                    <pre><code>{{ item.example.before }}</code></pre>
                  </div>
                  <div class="after">
                    <h5>优化后</h5>
                    <pre><code>{{ item.example.after }}</code></pre>
                  </div>
                </div>
              </el-collapse-item>
            </el-collapse>
          </div>
        </div>
      </div>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="auditDialogVisible = false">关闭</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 加载中遮罩 -->
    <el-loading
      v-model:full-screen="fullscreenLoading"
      text="合约审核中..."
    />
  </div>
</template>

<script lang="ts" setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Search } from '@element-plus/icons-vue'
import { getContractList, submitContract, verifyContractCode, getTransactionInfo } from '@/api/contract'

// 搜索和筛选相关
const searchQuery = ref('')
const statusFilter = ref('')
const handleSearch = () => {
  currentPage.value = 1 // 重置页码
  loadTableData()
}

// 编辑器相关
const editorLanguage = ref('solidity')

// 表单数据
const formRef = ref()
const formData = reactive({
  address: '',
  txHash: '',
  name: '',
  description: '',
  sourceCode: '',
  version: '0.8.17',
  optimization: true
})

// 表单验证规则
const rules = {
  address: [{ required: true, message: '请输入合约地址', trigger: 'blur' }],
  txHash: [{ required: true, message: '请输入交易哈希', trigger: 'blur' }],
  name: [{ required: true, message: '请输入合约名称', trigger: 'blur' }],
  version: [{ required: true, message: '请选择合约版本', trigger: 'change' }],
  sourceCode: [{ required: true, message: '请输入合约代码', trigger: 'blur' }]
}

// 验证合约
const verificationResult = ref(null)
const verifyContract = async () => {
  try {
    const res = await verifyContractCode({
      address: formData.address,
      sourceCode: formData.sourceCode,
      version: formData.version,
      optimization: formData.optimization
    })
    verificationResult.value = res
    if (res.success) {
      ElMessage.success('合约验证成功')
    }
  } catch (error) {
    ElMessage.error('合约验证失败')
  }
}

// 获取交易信息
const fetchTxInfo = async () => {
  if (!formData.txHash) {
    ElMessage.warning('请输入交易哈希')
    return
  }
  try {
    const res = await getTransactionInfo(formData.txHash)
    if (res.data) {
      formData.address = res.data.contractAddress
      ElMessage.success('获取交易信息成功')
    }
  } catch (error) {
    ElMessage.error('获取交易信息失败')
  }
}

// 审核结果相关
const auditDialogVisible = ref(false)
const fullscreenLoading = ref(false)
const auditResult = ref({
  status: 0,
  address: '',
  name: '',
  submitTime: '',
  details: null
})

// 提交表单
const handleSubmit = async () => {
  try {
    fullscreenLoading.value = true
    const [error, response] = await submitContract(formData)
    if (error) throw error

    // 直接添加到表格顶部，状态为审核中
    const newRecord = {
      id: response.data.id,
      address: formData.address,
      name: formData.name,
      submitTime: new Date().toISOString(),
      status: 0, // 审核中
      comment: '审核中...'
    }
    tableData.value.unshift(newRecord)
    total.value += 1

    // 模拟5秒后审核完成
    setTimeout(async () => {
      try {
        // 模拟发现安全漏洞
        const auditDetails = {
          securityChecks: [
            {
              title: '重入攻击风险',
              severity: 'error',
              description: '检测到可能存在重入攻击风险的代码模式',
              location: {
                line: 42,
                code: 'function withdraw() public {\n    uint amount = balances[msg.sender];\n    (bool success, ) = msg.sender.call{value: amount}("");\n    balances[msg.sender] = 0;\n}'
              }
            }
          ],
          codeQuality: [
            {
              type: 'warning',
              title: '函数可见性优化',
              suggestion: '建议明确指定所有函数的可见性'
            }
          ],
          gasOptimization: [
            {
              title: '存储优化',
              description: '使用 uint256 替代 uint8 可以节省 gas',
              example: {
                before: 'uint8[] public numbers;',
                after: 'uint256[] public numbers;'
              }
            }
          ]
        }

        // 只更新这条记录
        const index = tableData.value.findIndex(item => item.id === newRecord.id)
        if (index !== -1) {
          tableData.value[index] = {
            ...newRecord,
            status: 2, // 审核失败
            comment: '发现安全漏洞',
            auditDetails
          }
        }

        // 显示审核结果弹窗
        auditResult.value = {
          status: 2,
          address: formData.address,
          name: formData.name,
          submitTime: newRecord.submitTime,
          details: auditDetails
        }
        auditDialogVisible.value = true
        ElMessage.warning('审核发现安全漏洞')
      } catch (error) {
        ElMessage.error('获取审核结果失败')
      }
    }, 5000)

  } catch (error) {
    ElMessage.error('提交失败')
  } finally {
    fullscreenLoading.value = false
  }
}

// 分页相关
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const tableData = ref([])
const tableLoading = ref(false)

// 格式化日期
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

// 表格状态筛选方法
const filterStatus = (value: string, row: any) => {
  return row.status === parseInt(value)
}

// 修改获取表格数据方法
const loadTableData = async () => {
  try {
    tableLoading.value = true
    const [error, response] = await getContractList({
      page: currentPage.value,
      pageSize: pageSize.value,
      query: searchQuery.value,
      status: statusFilter.value // 添加状态筛选
    })
    if (error) throw error
    tableData.value = response.data.list
    total.value = response.data.total
  } catch (error) {
    ElMessage.error('获取数据失败')
  } finally {
    tableLoading.value = false
  }
}

// 状态展示相关
const getStatusType = (status: number) => {
  const map = {
    0: 'info',    // 待审核
    1: 'success', // 通过
    2: 'danger'   // 拒绝
  }
  return map[status] || 'info'
}

const getStatusText = (status: number) => {
  const map = {
    0: '待审核',
    1: '已通过',
    2: '已拒绝'
  }
  return map[status] || '未知'
}

// 其他事件处理器
const handleSizeChange = () => loadTableData()
const handleCurrentChange = () => loadTableData()
const handleView = async (row: any) => {
  try {
    // 实际应该调用后端接口获取详细信息
    // GET /api/contracts/{id}/audit-result
    // 返回格式应该与提交审核时的结果格式一致，包含：
    // {
    //   status: number,
    //   address: string,
    //   name: string,
    //   submitTime: string,
    //   details: {
    //     securityChecks: Array<{
    //       title: string,
    //       severity: 'error' | 'warning' | 'info',
    //       description: string,
    //       location?: {
    //         line: number,
    //         code: string
    //       }
    //     }>,
    //     codeQuality: Array<{
    //       type: string,
    //       title: string,
    //       suggestion: string
    //     }>,
    //     gasOptimization: Array<{
    //       title: string,
    //       description: string,
    //       example?: {
    //         before: string,
    //         after: string
    //       }
    //     }>
    //   }
    // }

    // 这里使用模拟数据
    auditResult.value = {
      status: row.status,
      address: row.address,
      name: row.name,
      submitTime: row.submitTime,
      details: row.auditDetails // 从表格数据中获取审核详情
    }
    auditDialogVisible.value = true
  } catch (error) {
    ElMessage.error('获取审核详情失败')
  }
}

// 获取代码质量建议的颜色
const getQualityColor = (type: string) => {
  const colors = {
    success: '#67C23A',
    warning: '#E6A23C',
    error: '#F56C6C',
    info: '#909399'
  }
  return colors[type] || colors.info
}

// 获取对话框标题
const getDialogTitle = (status: number) => {
  const map = {
    0: '审核中',
    1: '审核通过',
    2: '审核未通过'
  }
  return map[status] || '未知状态'
}

// 在组件挂载时加载历史记录
onMounted(() => {
  loadTableData()
})
</script>

<style lang="scss" scoped>
.contract-audit {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: calc(100vh - 40px);

  .operation-bar {
    margin-bottom: 20px;
    display: flex;
    justify-content: space-between;
  }

  .main-content {
    display: flex;
    gap: 20px;
    margin-bottom: 20px;

    .editor-section {
      flex: 1;
      background-color: #fff;
      border-radius: 4px;
      padding: 20px;
    }

    .form-section {
      width: 400px;
      background-color: #fff;
      border-radius: 4px;
      padding: 20px;
    }
  }

  .section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
    
    span {
      font-size: 16px;
      font-weight: 500;
    }

    .editor-tools {
      display: flex;
      gap: 8px;
    }
  }

  .table-section {
    background-color: #fff;
    border-radius: 4px;
    padding: 20px;
  }

  .verification-result {
    margin-top: 16px;
  }

  .pagination-container {
    margin-top: 20px;
    display: flex;
    justify-content: flex-end;
  }

  .audit-result {
    .info-section {
      margin-bottom: 20px;
    }

    .auditing-section {
      margin-bottom: 20px;
    }

    .success-section {
      margin-bottom: 20px;
    }

    .result-section {
      h3, h4 {
        margin: 16px 0;
        color: #303133;
      }

      .security-checks {
        .check-item {
          margin-bottom: 12px;

          :deep(.el-alert__description) {
            white-space: pre-line;
            font-family: monospace;
            margin-top: 8px;
            line-height: 1.6;
          }

          :deep(.el-alert__content) {
            padding: 8px 0;
          }

          .code-location {
            margin-top: 8px;
            pre {
              background-color: #f5f7fa;
              padding: 12px;
              border-radius: 4px;
              margin: 8px 0;
              font-size: 13px;
            }
          }
        }
      }

      .code-quality {
        margin: 20px 0;
      }

      .gas-optimization {
        .code-comparison {
          display: flex;
          gap: 20px;
          margin-top: 12px;

          .before, .after {
            flex: 1;
            
            h5 {
              margin-bottom: 8px;
              color: #606266;
            }

            pre {
              background-color: #f5f7fa;
              padding: 12px;
              border-radius: 4px;
            }
          }
        }
      }

      .regulations {
        margin: 20px 0;
        
        .regulation-card {
          .regulation-item {
            &:not(:last-child) {
              margin-bottom: 16px;
              padding-bottom: 16px;
              border-bottom: 1px solid #ebeef5;
            }
            
            h5 {
              color: #303133;
              margin-bottom: 8px;
            }
            
            .regulation-content {
              color: #606266;
              line-height: 1.6;
              margin-bottom: 8px;
            }
            
            .regulation-violation {
              color: #f56c6c;
              font-size: 14px;
            }
          }
        }
      }
    }
  }
}
</style> 