<template>
  <el-dialog v-model="visible" width="400px" :title="type === 'add' ? '新增角色' : '修改角色'">
    <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
      <el-form-item label="角色" prop="role">
        <el-input v-model="form.role"></el-input>
      </el-form-item>
      <el-form-item label="备注">
        <el-input v-model="form.remark"></el-input>
      </el-form-item>
      <el-form-item label="父级角色">
        <el-tree-select v-model="form.parent" :data="roleList" clearable :props="{ children: 'children', label: 'role', value: 'id' }" :render-after-expand="false" @node-click="treeNodeClick" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submit">确认</el-button>
      </el-form-item>
    </el-form>
  </el-dialog>
</template>

<script lang="ts" setup>
import { AnyObj, useCompRef, WritableDeep } from '@/utils/type';
import { ElForm, ElMessage } from 'element-plus';
import { reactive, ref, watch } from 'vue';
import { api_addRole, api_getRoleList, api_modifyRole } from '@/api/permissions';
import { dataToTree, deleteEmpty } from '@/utils/object';

const props = defineProps<{
  type: 'add' | 'modify'
  info?: AnyObj
  need?: AnyObj
}>()

const visible = ref(false);
const intailForm = Object.freeze({
  role: '',
  remark: '',
  parent: '',
})
const form: WritableDeep<typeof intailForm> = reactive(Object.assign({}, intailForm));
const rules = {
  role: { required: true, message: '请输入角色', trigger: 'blur' }
}
const formRef = useCompRef(ElForm);

const roleList = ref([]);
async function getRoleList() {
  const [err, res] = await api_getRoleList({});
  if (err) return;
  roleList.value = dataToTree(res.data);
}

function treeNodeClick(row) {
  form.parent = row.id;
}

watch(() => visible.value, value => {
  if (value) {
    getRoleList();
    if (props.type === 'modify') {
      for (const key in props.info) {
        form[key] = props.info[key];
      }
    }
  } else {
    for (const key in form) {
      form[key] = intailForm[key];
    }
    formRef.value.clearValidate();
  }
})

const emit = defineEmits(['success']);

function submit() {
  formRef.value.validate(async valid => {
    if (!valid) return;
    props.type === 'add' && create();
    props.type === 'modify' && modify();
  })
}

async function create() {
  const [err] = await api_addRole(deleteEmpty(form));
  if (err) return;
  ElMessage.success('添加成功');
  visible.value = false;
  emit('success');
}

async function modify() {
  const params = deleteEmpty({
    ...props.need,
    ...form,
  });
  const [err] = await api_modifyRole(params);
  if (err) return;
  ElMessage.success('修改成功');
  visible.value = false;
  emit('success');
}

defineExpose({ visible });
</script>