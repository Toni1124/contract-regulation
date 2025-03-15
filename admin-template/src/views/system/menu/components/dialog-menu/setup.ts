import { deleteEmpty } from "@/utils/object";
import { AnyObj } from "@/utils/type";
import { api_addMenu, api_modifyMenu } from "@/api/permissions";
import { ElMessage, FormInstance } from "element-plus";
import { getCurrentInstance, inject, reactive, ref, watch } from "vue"

export default () => {

  const current = getCurrentInstance();
  const props: AnyObj = current.props;

  const visible = ref(false);

  // const getMenuList: Function = inject('getMenuList')
  const menuList = ref([]);

  const form = reactive({
    name: '',
    title: '',
    parent: '',
  })

  const rules = {
    title: { required: true, message: '请输入菜单名称', trigger: 'blur' },
    name: { required: true, message: '请输入Name', trigger: 'blur' },
  }

  async function submit() {
    const el = current.refs.formRef as FormInstance;
    el.validate(async valid => {
      if (!valid) return;
      props.type === 0 ? addMenu() : modifyMenu();
    })
  }

  async function addMenu() {
    const params = deleteEmpty(form);
    const [err] = await api_addMenu(params);
    if (err) return;
    visible.value = false;
    ElMessage.success('添加成功');
    current.emit('success');
  } 

  async function modifyMenu() {
    const params = deleteEmpty({
      id: props.need.id,
      ...form,
    });
    const [err] = await api_modifyMenu(params);
    if (err) return;
    visible.value = false;
    ElMessage.success('修改成功');
    current.emit('success');
  } 

  const getMenuList: Function = inject('getMenuList');
  watch(() => visible.value, value => {
    if (value) {
      menuList.value = getMenuList();
      if (props.type === 1) {
        for (const prop in form) {
          form[prop] = props.need[prop];
        }
      }
    } else {
      (current.refs.formRef as FormInstance).resetFields();
      for (const prop in form) {
        form[prop] = '';
      }
    }
  })


  function treeNodeClick(row) {
    form.parent = row.id;
  }

  return {
    visible,
    menuList,

    form,
    rules,
    submit,

    treeNodeClick,
  }
}