<template>
  <div class="rule-edit">
    <div class="page-header">
      <h2>{{ isEdit ? '编辑规则' : '新增规则' }}</h2>
      <div class="actions">
        <el-button @click="handleCancel">取消</el-button>
        <el-button type="primary" @click="handleSubmit">保存</el-button>
      </div>
    </div>

    <div class="main-content">
      <!-- 左侧：规则表单 -->
      <div class="form-section">
        <el-form :model="form" :rules="rules" ref="formRef" label-width="140px">
          <el-form-item label="监管用户" prop="owner">
            <el-input v-model="form.owner" disabled />
          </el-form-item>
          <el-form-item label="监管规则名称" prop="name">
            <el-input v-model="form.name" placeholder="请输入规则名称" />
          </el-form-item>
          <el-form-item label="被监管合约地址" prop="contractAddress">
            <el-input v-model="form.contractAddress" placeholder="请输入合约地址">
              <template #append>
                <el-button @click="selectContract">选择合约</el-button>
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

          <!-- 函数规则列表 -->
          <div v-for="(func, funcIndex) in form.functions" :key="funcIndex" class="function-item">
            <div class="function-header">
              <h3>函数 {{ funcIndex + 1 }}</h3>
              <el-button type="danger" circle @click="removeFunction(funcIndex)">
                <el-icon><Delete /></el-icon>
              </el-button>
            </div>

            <el-form-item :label="'函数名称'" :prop="'functions.' + funcIndex + '.name'">
              <el-input v-model="func.name" placeholder="请输入函数名称" />
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
                    style="width: 100px"
                  >
                    <el-option label="=" value="=" />
                    <el-option label=">" value=">" />
                    <el-option label=">=" value=">=" />
                    <el-option label="<" value="<" />
                    <el-option label="<=" value="<=" />
                    <el-option label="!=" value="!=" />
                  </el-select>
                  <el-input
                    v-model="param.value"
                    placeholder="参数值"
                    style="width: 200px"
                  />
                  <el-button type="danger" circle @click="removeParam(funcIndex, paramIndex)">
                    <el-icon><Delete /></el-icon>
                  </el-button>
                </div>
              </el-form-item>
            </div>

            <el-button type="primary" plain @click="addParam(funcIndex)">
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

      <!-- 右侧：合约源码 -->
      <div v-if="selectedContract" class="contract-section">
        <div class="contract-header">
          <h3>合约源码</h3>
          <p class="contract-info">
            <span>名称：{{ selectedContract.name }}</span>
            <span>地址：{{ selectedContract.address }}</span>
          </p>
        </div>
        <div class="source-code">
          <pre><code>{{ selectedContract.sourceCode }}</code></pre>
        </div>
      </div>
    </div>

    <!-- 选择合约弹窗 -->
    <el-dialog
      v-model="contractDialogVisible"
      title="选择合约"
      width="800px"
    >
      <div class="contract-search">
        <el-input
          v-model="contractSearch"
          placeholder="搜索合约名称或地址"
          clearable
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
      </div>

      <el-table
        :data="filteredContracts"
        style="width: 100%"
        @row-click="handleContractSelect"
      >
        <el-table-column prop="name" label="合约名称" />
        <el-table-column prop="address" label="合约地址" width="360" />
        <el-table-column label="操作" width="100">
          <template #default="{ row }">
            <el-button link type="primary" @click="handleContractSelect(row)">
              选择
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Delete, Plus, Search } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const isEdit = computed(() => route.query.id !== undefined)

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

// 合约相关
const contractDialogVisible = ref(false)
const contractSearch = ref('')
const selectedContract = ref<any>(null)

// 示例合约数据
const contracts = ref([
  {
    id: 1,
    name: 'TokenContract',
    address: '0x1234567890abcdef1234567890abcdef12345678',
    sourceCode: `contract TokenContract {
    uint256 public totalSupply;
    mapping(address => uint256) public balances;
    
    function transfer(address to, uint256 amount) public {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        balances[msg.sender] -= amount;
        balances[to] += amount;
    }
    
    function mint(address to, uint256 amount) public {
        totalSupply += amount;
        balances[to] += amount;
    }
}`
  }
])

const filteredContracts = computed(() => {
  const search = contractSearch.value.toLowerCase()
  return contracts.value.filter(contract => 
    contract.name.toLowerCase().includes(search) ||
    contract.address.toLowerCase().includes(search)
  )
})

// 函数操作
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

// 合约选择
const selectContract = () => {
  contractDialogVisible.value = true
}

const handleContractSelect = (contract: any) => {
  selectedContract.value = contract
  form.value.contractAddress = contract.address
  contractDialogVisible.value = false
}

// 表单操作
const handleSubmit = async () => {
  try {
    // 这里应该调用保存API
    ElMessage.success(isEdit.value ? '更新成功' : '添加成功')
    router.push('/rule-management')
  } catch (error) {
    console.error('操作失败:', error)
    ElMessage.error('操作失败，请重试')
  }
}

const handleCancel = () => {
  router.push('/rule-management')
}

// 初始化
onMounted(async () => {
  if (isEdit.value) {
    // 这里应该调用获取详情API
    const mockData = {
      id: route.query.id,
      name: '转账金额限制规则',
      contractAddress: '0x1234567890abcdef1234567890abcdef12345678',
      description: '限制单次转账金额不超过1000 ETH',
      owner: 'super',
      functions: [
        {
          name: 'transfer',
          params: [
            {
              name: 'amount',
              type: 'uint256',
              condition: '<=',
              value: '1000000000000000000000'
            }
          ]
        }
      ]
    }
    form.value = mockData
    // 获取合约详情
    selectedContract.value = contracts.value[0]
  }
})
</script>

<style lang="scss" scoped>
.rule-edit {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: calc(100vh - 40px);

  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    background-color: #fff;
    padding: 16px 20px;
    border-radius: 4px;

    h2 {
      margin: 0;
      font-size: 20px;
      font-weight: 500;
    }

    .actions {
      display: flex;
      gap: 10px;
    }
  }

  .main-content {
    display: flex;
    gap: 20px;

    .form-section {
      flex: 1;
      background-color: #fff;
      padding: 20px;
      border-radius: 4px;
    }

    .contract-section {
      width: 500px;
      background-color: #fff;
      padding: 20px;
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
        background-color: #f5f7fa;
        padding: 16px;
        border-radius: 4px;
        max-height: calc(100vh - 250px);
        overflow-y: auto;

        pre {
          margin: 0;
          white-space: pre-wrap;
          word-wrap: break-word;

          code {
            font-family: monospace;
            font-size: 14px;
            line-height: 1.5;
          }
        }
      }
    }
  }

  .function-item {
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

  .contract-search {
    margin-bottom: 16px;
  }
}
</style> 