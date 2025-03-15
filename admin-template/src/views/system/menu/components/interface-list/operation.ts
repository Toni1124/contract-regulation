import { deleteEmpty } from "@/utils/object";
import { AnyObj } from "@/utils/type";
import { api_batchSynchronization, api_deleteInterface } from "@/api/permissions";
import { ElMessage, ElMessageBox } from "element-plus";
import { getCurrentInstance, ref } from "vue";

export default () => {

  const current = getCurrentInstance();
  const _this: AnyObj = current.proxy;
  const props: AnyObj = current.props;

  const dialogInterfaceType = ref(0);
  const dialogInterfaceNeed = ref({});

  /**
   * 添加接口
   */
  function addInterface() {
    dialogInterfaceType.value = 0;
    dialogInterfaceNeed.value = { menuId: props.menuId };
    (current.refs.dialogInterface as any).visible = true;
  }

  /**
   * 修改接口
   */
  function modifyInterface(row) {
    const { id, name, method, url, menuId } = row;
    dialogInterfaceType.value = 1;
    dialogInterfaceNeed.value = { id, name, method, url, menuId };
    (current.refs.dialogInterface as any).visible = true;
  }

  /**
   * 删除接口
   */
  function deleteInterface(row) {
    ElMessageBox.confirm('确认删除该接口', '提示', {
      confirmButtonText: '确认',
      cancelButtonText: '取消',
      type: 'warning',
    }).then(async () => {
      const [err, res] = await api_deleteInterface({ id: row.id });
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
      tableType: 'interface',
      roleId: props.roleId,
      contactIdList,
      deleteIdList,
    })
    const [err] = await api_batchSynchronization(params);
    if (err) return;
    _this.initData();
  }

  return {
    dialogInterfaceType,
    dialogInterfaceNeed,
    addInterface,
    modifyInterface,
    deleteInterface,

    select,
  }
}