<template>
  <div>
    <el-table :data="listData" style="width: 100%">
      <el-table-column prop="address" label="账户地址" />
      <el-table-column prop="operator" label="操作人" />
      <el-table-column prop="type" label="类型">
        <template #default="{ row }">
          {{ row.type === 1 ? '白名单' : '黑名单' }}
        </template>
      </el-table-column>
      <el-table-column prop="organization" label="发布机构" />
      <el-table-column prop="region" label="使用范围" />
    </el-table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getBlackWhiteList } from '@/api/blackWhiteList'

const listData = ref([])

const fetchData = async () => {
  try {
    const response = await getBlackWhiteList()
    listData.value = response.data.data.list
  } catch (error) {
    console.error('获取数据失败:', error)
  }
}

onMounted(() => {
  fetchData()
})
</script> 