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

    <!-- 注册记录表格 -->
    <div class="table-section" style="margin-top: 20px;">
      <div class="section-header">
        <span>注册记录</span>
      </div>
      <el-table :data="registeredContracts" border style="width: 100%">
        <el-table-column prop="name" label="合约名称" min-width="180" />
        <el-table-column prop="address" label="合约地址" min-width="280">
          <template #default="{ row }">
            <el-tooltip :content="row.address" placement="top" :show-after="500">
              <span class="address-text">{{ row.address }}</span>
            </el-tooltip>
          </template>
        </el-table-column>
        <el-table-column prop="txHash" label="交易哈希" min-width="280">
          <template #default="{ row }">
            <el-tooltip :content="row.txHash" placement="top" :show-after="500">
              <span class="address-text">{{ row.txHash }}</span>
            </el-tooltip>
          </template>
        </el-table-column>
        <el-table-column prop="registerTime" label="注册时间" min-width="180">
          <template #default="{ row }">
            {{ formatDate(row.registerTime) }}
          </template>
        </el-table-column>
      </el-table>
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
            <el-descriptions-item label="合约名称">{{ auditResult.name }}</el-descriptions-item>
            <el-descriptions-item label="提交时间">{{ formatDate(auditResult.submitTime) }}</el-descriptions-item>
            <el-descriptions-item label="审核状态" :span="2">
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

        <!-- 审核未通过状态 - 详细风险展示 -->
        <div v-else-if="auditResult.status === 2 && auditResult.details" class="result-section">
          <h3>审核详情</h3>
          <div v-if="auditResult.details.securityChecks?.length" class="security-checks">
            <div v-for="(check, index) in auditResult.details.securityChecks" :key="index" class="check-item">
              <el-card class="check-card">
                <template #header>
                  <div class="check-header">
                    <el-tag :type="check.severity === 'high' ? 'danger' : 'warning'" effect="dark">
                      {{ check.severity.toUpperCase() }}
                    </el-tag>
                    <span class="check-title">{{ check.title }}</span>
                  </div>
                </template>
                <div class="check-content">
                  <div class="check-info">
                    <div class="info-item">
                      <strong>检查类型：</strong>
                      <span>{{ check.check }}</span>
                    </div>
                    <div class="info-item">
                      <strong>置信度：</strong>
                      <span>{{ check.confidence }}</span>
                    </div>
                  </div>
                  <div class="check-description">
                    <strong>问题描述：</strong>
                    <pre>{{ check.description }}</pre>
                  </div>
                  <div v-if="check.location" class="code-location">
                    <strong>问题位置：</strong>
                    <p>第 {{ check.location.line }} 行</p>
                    <pre v-if="check.location.code"><code>{{ check.location.code }}</code></pre>
                  </div>
                </div>
              </el-card>
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
          <el-button 
            v-if="auditResult.status === 1" 
            type="primary" 
            @click="registerDialogVisible = true"
          >
            注册合约
          </el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 添加注册合约弹窗 -->
    <el-dialog
      v-model="registerDialogVisible"
      title="注册合约"
      width="50%"
      :close-on-click-modal="false"
    >
      <el-form 
        ref="registerFormRef"
        :model="registerForm"
        :rules="registerRules"
        label-width="100px"
      >
        <el-form-item label="合约地址" prop="address">
          <el-input v-model="registerForm.address" placeholder="请输入已部署的合约地址" />
        </el-form-item>
        
        <el-form-item label="交易哈希" prop="txHash">
          <el-input v-model="registerForm.txHash" placeholder="部署合约的交易哈希" />
        </el-form-item>
      </el-form>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="registerDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitRegister">提交注册</el-button>
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
import { submitContractAudit, getAuditList, registerContract, getRegisteredContracts, getAuditDetail } from '@/api/contractAudit'

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
  name: '',
  description: '',
  sourceCode: '',
  version: '0.8.17'
})

// 表单验证规则
const rules = {
  name: [{ required: true, message: '请输入合约名称', trigger: 'blur' }],
  version: [{ required: true, message: '请选择合约版本', trigger: 'change' }],
  sourceCode: [{ required: true, message: '请输入合约代码', trigger: 'blur' }]
}

// 验证合约
const verificationResult = ref(null)

// 审核结果相关
const auditDialogVisible = ref(false)
const fullscreenLoading = ref(false)
const auditResult = ref<{
  id: number,
  status: number
  name: string
  submitTime: string
  address: string
  details: {
    securityChecks: SecurityCheck[]
  } | null
}>({
  id: 0,
  status: 0,
  name: '',
  submitTime: '',
  address: '',
  details: null
})

// 提交表单
const handleSubmit = async () => {
  try {
    fullscreenLoading.value = true
    const response = await submitContractAudit({
      name: formData.name,
      source_code: formData.sourceCode,
      version: formData.version
    })

    if (response.code !== 200) {
      throw new Error(response.message)
    }

    // 添加到表格顶部
    const newRecord = {
      id: response.data.auditId!,
      name: formData.name,
      submitTime: new Date().toISOString(),
      status: response.data.success ? 1 : 2,
      comment: response.data.success ? '审核通过' : '发现安全漏洞'
    }
    tableData.value.unshift(newRecord)
    total.value += 1

    // 显示审核结果弹窗
    auditResult.value = {
      id: response.data.auditId,
      status: response.data.success ? 1 : 2,
      name: formData.name,
      submitTime: newRecord.submitTime,
      address: '',
      details: response.data.auditDetails ? {
        securityChecks: response.data.auditDetails.securityChecks.map(detail => ({
          title: detail.title,
          severity: detail.severity.toLowerCase(),
          description: detail.description,
          check: detail.check,
          confidence: detail.confidence,
          location: detail.location
        }))
      } : null
    }
    auditDialogVisible.value = true

    if (!response.data.success) {
      ElMessage.warning('审核发现安全漏洞')
    } else {
      ElMessage.success('审核通过')
    }

  } catch (error) {
    ElMessage.error(error instanceof Error ? error.message : '提交失败')
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
    const response = await getAuditList({
      page: currentPage.value,
      pageSize: pageSize.value,
      query: searchQuery.value,
      status: statusFilter.value ? Number(statusFilter.value) : undefined
    })

    if (response.code === 200) {
      tableData.value = response.data.list.map(item => ({
        id: item.id,
        name: item.name,
        submitTime: item.submit_time,
        status: item.audit_status,
        comment: getStatusText(item.audit_status),
        auditDetails: item.audit_result
      }))
      total.value = response.data.total
    } else {
      throw new Error(response.message)
    }
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
    const response = await getAuditDetail(row.id)
    
    if (response.code === 200) {
      auditResult.value = {
        id: response.data.id,
        status: response.data.audit_status,
        name: response.data.name,
        submitTime: response.data.submit_time,
        address: '',
        details: response.data.audit_result
      }
      auditDialogVisible.value = true
    } else {
      throw new Error(response.message)
    }
  } catch (error) {
    console.error('Error fetching audit detail:', error)
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

// 添加注册相关的数据和方法
const registerDialogVisible = ref(false)
const registerFormRef = ref()
const registerForm = reactive({
  address: '',
  txHash: ''
})

const registerRules = {
  address: [{ required: true, message: '请输入合约地址', trigger: 'blur' }],
  txHash: [{ required: true, message: '请输入交易哈希', trigger: 'blur' }]
}

// 提交注册
const submitRegister = async () => {
  if (!registerFormRef.value) return
  
  await registerFormRef.value.validate(async (valid: boolean) => {
    if (valid) {
      try {
        const response = await registerContract(auditResult.value.id, {
          address: registerForm.address,
          tx_hash: registerForm.txHash
        })
        
        if (response.code === 200) {
          ElMessage.success('合约注册成功')
          registerDialogVisible.value = false
          auditDialogVisible.value = false
          loadTableData() // 刷新审核记录
          loadRegisteredContracts() // 刷新注册记录
        } else {
          throw new Error(response.message)
        }
      } catch (error) {
        ElMessage.error(error instanceof Error ? error.message : '注册失败')
      }
    }
  })
}

// 添加注册记录的响应式数据
const registeredContracts = ref([])
const loadRegisteredContracts = async () => {
  try {
    const response = await getRegisteredContracts({
      page: currentPage.value,
      pageSize: pageSize.value
    })
    if (response.code === 200) {
      registeredContracts.value = response.data.list.map(item => ({
        id: item.id,
        name: item.name,
        address: item.address,
        txHash: item.tx_hash,
        registerTime: item.register_time
      }))
    }
  } catch (error) {
    ElMessage.error('获取注册记录失败')
  }
}

// 在组件挂载时加载两个表格的数据
onMounted(() => {
  loadTableData()
  loadRegisteredContracts()
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
          margin-bottom: 24px;

          .check-card {
            .check-header {
              display: flex;
              align-items: center;
              gap: 12px;

              .check-title {
                font-size: 16px;
                font-weight: 500;
              }
            }

            .check-content {
              .check-info {
                display: flex;
                gap: 24px;
                margin-bottom: 16px;

                .info-item {
                  display: flex;
                  align-items: center;
                  gap: 8px;
                }
              }

              .check-description {
                margin-bottom: 16px;

                pre {
                  margin-top: 8px;
                  padding: 16px;
                  background-color: #f8f9fb;
                  border-radius: 4px;
                  white-space: pre-wrap;
                  word-wrap: break-word;
                  font-family: monospace;
                  font-size: 14px;
                  line-height: 1.6;
                }
              }

              .code-location {
                p {
                  margin: 8px 0;
                }

                pre {
                  margin-top: 8px;
                  padding: 16px;
                  background-color: #1e1e1e;
                  color: #d4d4d4;
                  border-radius: 4px;
                  overflow-x: auto;
                  font-family: monospace;
                  font-size: 14px;
                  line-height: 1.6;
                }
              }
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