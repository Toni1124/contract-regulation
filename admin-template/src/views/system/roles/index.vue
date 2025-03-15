<template>
  <LayoutContainer>
    <LayoutSearch right-width="320px">
      <template #left>
        <el-input v-model="form.role" placeholder="请输入角色" @keyup.enter="search" @clear="search" />
      </template>
      <template #right>
        <el-button type="primary" @click="search">查询</el-button>
        <el-button @click="reset">重置</el-button>
        <el-button type="primary" @click="addRole">新增</el-button>
      </template>
    </LayoutSearch>

    <el-table :data="tableData" row-key="id" :tree-props="{children: 'children'}">
      <el-table-column type="index" label="序号" width="60" />
      <el-table-column label="角色" prop="role" />
      <el-table-column label="备注" prop="remark" />
      <el-table-column label="操作" fixed="right" width="100">
        <template #default="{ row }">
          <el-link @click="modifyRole(row)">修改</el-link>
          <el-link type="danger" @click="deleteRole(row)">删除</el-link>
        </template>
      </el-table-column>
    </el-table>

    <DialogEdit ref="dialogEditRef" :type="dialogEditType" :info="dialogEditInfo" :need="dialogEditNeed" @success="initData" />
  </LayoutContainer>
</template>

<script lang="ts">
import DialogEdit from './components/dialog-edit/index.vue';
import { InitTable } from '@/utils/init-table';
import { api_getRoleList, api_deleteRole } from '@/api/permissions';
import { ref } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { dataToTree, deleteEmpty } from '@/utils/object';

export default {
  name: 'SystemRoles',
  components: {
    DialogEdit,
  },
  setup() {
    const searchForm = {
      role: '',
    }
    class Init extends InitTable<typeof searchForm> {
      constructor() {
        super(searchForm);
        this.initData();
      }

      initData = async () => {
        const params = deleteEmpty(this.form);
        const [err, res] = await api_getRoleList(params);
        if (err) {
          this.tableData.value = [];
        } else {
          this.tableData.value = dataToTree(res.data || []);
        }
      }
    }
    const init = new Init();

    const dialogEditRef = ref();
    const dialogEditType = ref<'add' | 'modify'>('add');
    const dialogEditInfo = ref({});
    const dialogEditNeed = ref({});
    function addRole() {
      dialogEditRef.value.visible = true;
      dialogEditInfo.value = {};
      dialogEditNeed.value = {};
      dialogEditType.value = 'add';
    }

    function modifyRole(row) {
      dialogEditType.value = 'modify';
      dialogEditInfo.value = {
        role: row.role,
        remark: row.remark,
        parent: row.parent,
      }
      dialogEditNeed.value = {
        id: row.id,
      }
      dialogEditRef.value.visible = true;
    }

    async function deleteRole(row) {
      let tips = row.children.length === 0 ? '确认删除该角色？' : '删除该角色子级也会被删除，请确认操作！';
      ElMessageBox.confirm(tips, '提示', {
        type: 'warning',
        confirmButtonText: '确认',
        cancelButtonText: '取消',
      }).then(async () => {
        const [err] = await api_deleteRole({ id: row.id });
        if (err) return;
        ElMessage.success('删除成功');
        init.initData();
      }).catch(() => {})
    }

    return {
      ...init,
      dialogEditRef,
      dialogEditType,
      dialogEditInfo,
      dialogEditNeed,
      addRole,
      modifyRole,
      deleteRole,
    }

  }
}


</script>
