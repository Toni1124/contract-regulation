import { deleteEmpty } from "@/utils/object";
import { AnyObj } from "@/utils/type";
import { api_batchSynchronization, api_deleteElement, api_deleteInterface } from "@/api/permissions";
import { ElMessage, ElMessageBox } from "element-plus";
import { getCurrentInstance, ref } from "vue";

export default () => {

  const current = getCurrentInstance();
  const _this: AnyObj = current.proxy;
  const props: AnyObj = current.props;

  const dialogElementType = ref(0);
  const dialogElementNeed = ref({});

  /**
   * 添加接口
   */
  function addElement() {
    dialogElementType.value = 0;
    dialogElementNeed.value = { menuId: props.menuId };
    (current.refs.dialogElement as any).visible = true;
  }

  /**
   * 修改接口
   */
  function modifyElement(row) {
    const { id, name, key, menuId } = row;
    dialogElementType.value = 1;
    dialogElementNeed.value = { id, name, key, menuId };
    (current.refs.dialogElement as any).visible = true;
  }

  /**
   * 删除接口
   */
  function deleteElement(row) {
    ElMessageBox.confirm('确认删除该元素', '提示', {
      confirmButtonText: '确认',
      cancelButtonText: '取消',
      type: 'warning',
    }).then(async () => {
      const [err, res] = await api_deleteElement({ id: row.id });
      if (err) return;
      ElMessage.success('删除成功');
      _this.initData();
    }).catch(() => {});
  }

  async function select(rows) {
    const contactIdList = rows.map(val => val.id);
    const deleteIdList = _this.tableData
      .filter(val => !contactIdList.includes(val.id))
      .map(val => val.id);
    const params = deleteEmpty({
      tableType: 'element',
      roleId: props.roleId,
      contactIdList,
      deleteIdList,
    })
    const [err] = await api_batchSynchronization(params);
    if (err) return;
    _this.initData();
  }

  return {
    dialogElementType,
    dialogElementNeed,
    addElement,
    modifyElement,
    deleteElement,

    select,
  }
}