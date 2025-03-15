<template>
  <div class="element-list">
    <LayoutSearchHeader right-width="340px">
      <template #left>
        <el-input v-model="form.name" placeholder="请输入元素名称" @keyup.enter="search" @clear="search" />
      </template>
      <template #right>
        <el-button type="primary" @click="search">查询</el-button>
        <el-button @click="reset">重置</el-button>
      </template>
    </LayoutSearchHeader>
    <el-table ref="tableEl" :data="tableData" @select="select" @select-all="select">
      <el-table-column type="selection" width="40" label="" />
      <el-table-column type="index" label="序号" width="60" />
      <el-table-column label="元素名称" prop="name" />
      <el-table-column label="Key" prop="key" />
      <el-table-column label="更新时间">
        <template #default="scope">
          {{ dateFormater((scope.row.updateTime || scope.row.createTime) * 1000) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" fixed="right" width="100">
        <template #default="scope">
          <el-link @click="modifyElement(scope.row)">修改</el-link>
          <el-link type="danger" @click="deleteElement(scope.row)">删除</el-link>
        </template>
      </el-table-column>
    </el-table>
    <TableAddBtn @click="addElement" />

    <DialogElement ref="dialogElement" :type="dialogElementType" :need="dialogElementNeed" @success="initData" />
    
  </div>
</template>

<script lang="ts">
import LayoutSearchHeader from '@/components/layout-search-header/index.vue'
import TableAddBtn from '../table-add-btn/index.vue';
import DialogElement from '../dialog-element/index.vue';

import { dateFormater } from '@/utils/date';
import { Init } from './init';
import operation from './operation';
export default {
  components: {
    LayoutSearchHeader,
    TableAddBtn,
    DialogElement,
  },
  props: {
    roleId: {
      type: [String, Number],
      required: true
    },
    menuId: {
      type: String,
      default: ''
    }
  },
  setup: () => ({
    dateFormater,
    ...new Init(),
    ...operation(),
  })
}
</script>
