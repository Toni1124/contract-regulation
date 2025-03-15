<template>
  <LayoutContainer>
    <template #header>
      <LayoutSearch>
        <template #left>
          <el-input v-model="form.name" class="input" @keyup.enter="search" @clear="search" />
        </template>
        
        <template #right>
          <el-button @click="search">查询</el-button>
          <el-button type="primary" @click="reset">重置</el-button>
        </template>
      </LayoutSearch>
      <h2>公共类：表格 搜索/分页 逻辑</h2>
    </template>

    <el-table :data="tableData" height="100%">
      <el-table-column label="序号" type="index" width="60">
        <template #default="scope">
          {{ pagingIndex(scope.$index) }}
        </template>
      </el-table-column>
      <el-table-column label="子链ID" prop="chainId" min-width="220" />
      <el-table-column label="子链名称" prop="name" />
      <el-table-column label="用户名" prop="byUserName" />
      <el-table-column label="标签" prop="tag" />
    </el-table>

    <template #footer>
      <el-pagination
        v-model:current-page="paging.pageNumber"
        v-model:page-size="paging.pageSize"
        :total="paging.total"
        @current-change="onCurrentChange"
        @size-change="onSizeChange"
      />
    </template>
  </LayoutContainer>

</template>

<script lang='ts'>
import { InitTable } from '@/utils/init-table';
import { api_getChainTradingList } from '@/api/test';

export default {
  // name: 'ExampleTable',
  setup() {
    const searchForm = {
      name: '',
    }
    class Init extends InitTable<typeof searchForm> {
      constructor() {
        super(searchForm, api_getChainTradingList);
        this.initData()
      }
    }

    const init = new Init();

    return {
      ...init,
    }
  }
}

</script>
