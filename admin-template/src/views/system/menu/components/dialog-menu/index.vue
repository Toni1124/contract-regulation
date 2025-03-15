<template>
  <el-dialog v-model="visible" width="400px" :title="type === 1 ? '修改菜单' : '新增菜单'">
    <el-form ref="formRef" label-width="100px" :model="form" :rules="rules">
      <el-form-item label="菜单名称" prop="title">
        <el-input v-model="form.title" />
      </el-form-item>
      <el-form-item label="Name" prop="name">
        <el-input v-model="form.name" placeholder="保证唯一，对应前端路由设置 name" />
      </el-form-item>
      <el-form-item label="父级菜单">
        <el-tree-select v-model="form.parent" :data="menuList" clearable :props="{ children: 'children', label: 'title', value: 'id' }" :render-after-expand="false" @node-click="treeNodeClick" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submit">确认</el-button>
      </el-form-item>
    </el-form>
  </el-dialog>
</template>

<script lang="ts">
import setup from './setup';
import { PropType } from 'vue';

export default {
  props: {
    type: {
      type: Number as PropType<0 | 1>,  // 0: 添加， 1: 修改
      default: 0,
    },
    need: {
      type: Object,
      default: () => ({}),
    }
  },
  setup
}
</script>