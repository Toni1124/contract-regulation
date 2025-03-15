<template>
  <div class="contract-detail">
    <div class="page-header">
      <h2>合约详情</h2>
      <div class="actions">
        <el-button @click="handleBack">返回</el-button>
        <el-button type="primary" @click="handleAddRule">添加规则</el-button>
      </div>
    </div>

    <div class="main-content">
      <div class="contract-info">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="合约名称">{{ contract.name }}</el-descriptions-item>
          <el-descriptions-item label="合约地址">{{ contract.address }}</el-descriptions-item>
        </el-descriptions>
      </div>

      <div class="source-code-section">
        <div class="section-header">
          <h3>源代码</h3>
        </div>
        <div class="code-container">
          <pre><code>{{ contract.sourceCode }}</code></pre>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

// 示例合约数据
const contract = ref({
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
})

const handleBack = () => {
  router.back()
}

const handleAddRule = () => {
  router.push(`/rule-management/edit?contractAddress=${contract.value.address}`)
}

onMounted(async () => {
  const address = route.query.address as string
  if (address) {
    // 这里应该调用获取合约详情API
    // const res = await getContractDetail(address)
    // contract.value = res.data
  }
})
</script>

<style lang="scss" scoped>
.contract-detail {
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
    background-color: #fff;
    border-radius: 4px;
    padding: 20px;

    .contract-info {
      margin-bottom: 20px;
    }

    .source-code-section {
      .section-header {
        margin-bottom: 16px;

        h3 {
          margin: 0;
          font-size: 16px;
          font-weight: 500;
          color: #303133;
        }
      }

      .code-container {
        background-color: #f5f7fa;
        padding: 16px;
        border-radius: 4px;
        max-height: calc(100vh - 300px);
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
}
</style> 