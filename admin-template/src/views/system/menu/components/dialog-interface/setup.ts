import { deleteEmpty } from "@/utils/object";
import { AnyObj } from "@/utils/type";
import { api_addInferface, api_modifyInferface } from "@/api/permissions";
import { ElMessage, FormInstance } from "element-plus";
import { getCurrentInstance, inject, reactive, ref, watch } from "vue"

export default () => {

  const current = getCurrentInstance();
  const props: AnyObj = current.props;

  const visible = ref(false);

  const form = reactive({
    name: '',
    method: '',
    url: '',
    menuId: '',
  })

  const rules = {
    name: { required: true, message: '请输入接口名称', trigger: 'blur' },
    method: { required: true, message: '请选择方法', trigger: 'blur' },
    url: { required: true, message: '请输入Url', trigger: 'blur' },
  }

  async function submit() {
    const el = current.refs.formRef as FormInstance;
    el.validate(async valid => {
      if (!valid) return;
      props.type === 0 ? addInterface() : modifyInterface();
    })
  }

  async function addInterface() {
    const params = deleteEmpty(form);
    const [err] = await api_addInferface(params);
    if (err) return;
    ElMessage.success('添加成功');
    visible.value = false;
    current.emit('success')
  }

  async function modifyInterface() {
    const params = deleteEmpty({
      id: props.need.id,
      ...form,
    });
    const [err] = await api_modifyInferface(params);
    if (err) return;
    ElMessage.success('修改成功');
    visible.value = false;
    current.emit('success')
  }

  const getRoleList: Function = inject('getRoleList');
  const getMenuList: Function = inject('getMenuList');
  const roleList = ref([]);
  const menuList = ref([]);

  watch(() => visible.value, value => {
    if (value) {
      roleList.value = getRoleList();
      menuList.value = getMenuList();
      if (props.type === 0) {
        form.menuId = props.need.menuId;
      }
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
    form.menuId = row.id;
  }

  return {
    visible,
    menuList,
    methodList: [
      { value: "GET" },
      { value: "POST" },
      { value: "PUT" },
      { value: "DELETE" },
      { value: "HEAD" },
      { value: "CONNECT" },
      { value: "OPTIONS" },
      { value: "TRACE" },
      { value: "PATCH" },
    ],

    form,
    rules,
    submit,

    treeNodeClick,
  }
}