<template>
  <LayoutContainer>
    <LayoutSearch right-width="320px">
      <template #left>
        <el-tree-select v-model="nowRole.id" :data="roleList" clearable :props="{ children: 'children', label: 'role', value: 'id' }" :render-after-expand="false" @node-click="treeNodeClick" />
        <el-input v-model="form.title" class="input" placeholder="请输入菜单名称" @keyup.enter="search" @clear="search" />
      </template>

      <template #right>
        <el-button type="primary" @click="search">查询</el-button>
        <el-button @click="reset">重置</el-button>
        <el-button type="primary" @click="showConfig()">公共配置</el-button>
      </template>
    </LayoutSearch>


    <el-table ref="tableEl" :data="tableData" row-key="id" :tree-props="{children: 'children'}" @select="select" @select-all="select">
      <el-table-column type="selection" width="40" label="" />
      <el-table-column type="index" label="序号" width="60" />
      <el-table-column label="菜单名称" prop="title" />
      <el-table-column label="Name" prop="name" />
      <el-table-column label="更新时间">
        <template #default="scope">
          {{ dateFormater((scope.row.updateTime || scope.row.createTime) * 1000) }}
        </template>
      </el-table-column>
      <el-table-column label="排序" fixed="right" width="80">
        <template #default="{ row }">
          <span class="sort-box">
            <el-link v-if="canMove(row, 'up')" @click="moveRow(row, 'up')" style="color: var(--main-color-font-success)">⬆︎</el-link>
          </span>
          <span class="sort-box">
            <el-link v-if="canMove(row, 'down')" @click="moveRow(row, 'down')" style="color: var(--main-color-font-error);">⬇︎</el-link>
          </span>
        </template>
      </el-table-column>
      <el-table-column label="操作" fixed="right" width="140">
        <template #default="{ row }"> 
          <el-link @click="showConfig(row)">配置</el-link>
          <el-link @click="modifyMenu(row)">修改</el-link>
          <el-link type="danger" @click="deleteMenu(row)">删除</el-link>
        </template>
      </el-table-column>
    </el-table>
    <TableAddBtn @click="addMenu" />

    <DrawerConfig ref="drawerConfig" :roleId="nowRole.id" :menuId="selectMenu.id" />
    <DialogMenu ref="dialogMenu" :type="dialogMenuType" :need="dialogMenuNeed" @success="initData" />

  </LayoutContainer>
</template>

<script lang='ts'>
import DrawerConfig from './components/drawer-config/index.vue';
import TableAddBtn from './components/table-add-btn/index.vue';
import DialogMenu from './components/dialog-menu/index.vue';

import { dateFormater } from '@/utils/date';
import Init from './init';
import operation from './operation';

export default {
  name: "SystemMenu",
  components: {
    DrawerConfig,
    TableAddBtn,
    DialogMenu,
  },
  setup() {
    return {
      dateFormater,
      ...new Init(),
      ...operation(),
    }
  }
}
</script>

<style lang="scss" scoped>
.sort-box{
  display: inline-block;
  width: 20px;
}
</style>