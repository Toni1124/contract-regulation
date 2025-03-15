import { AnyObj } from "@/utils/type";
import { api_batchSynchronization, api_deleteMenu, api_modifyOrder } from "@/api/permissions";
import { ElMessage, ElMessageBox } from "element-plus";
import { getCurrentInstance, reactive, ref } from "vue"


export default () => {

  const current = getCurrentInstance();
  const _this: AnyObj = current.proxy;

  const selectMenu = reactive({ name: '', id: '' });

  function showConfig(row: AnyObj = {}) {
    selectMenu.name = row.name;
    selectMenu.id = row.id;
    (current.refs.drawerConfig as any).visible = true;
  }

  const dialogMenuType = ref<0 | 1>(0);
  const dialogMenuNeed = ref({});

  function addMenu() {
    dialogMenuType.value = 0;
    dialogMenuNeed.value = {};
    (current.refs.dialogMenu as any).visible = true;
  }

  function modifyMenu(row) {
    const { id, name, title, parent } = row;
    dialogMenuType.value = 1;
    dialogMenuNeed.value = { id, name, title, parent };
    (current.refs.dialogMenu as any).visible = true;
  }

  function deleteMenu(row) {
    ElMessageBox.confirm('确认删除该用户？删除后配置中的接口/元素会归类到公共配置中！', '提示', {
      confirmButtonText: '确认',
      cancelButtonText: '取消',
      type: 'warning',
    }).then(async () => {
      const [err, res] = await api_deleteMenu({ id: row.id });
      if (err) return;
      ElMessage.success('删除成功');
      _this.initData();
    }).catch(() => {});
  }

  async function select(rows) {
    const contactIdList = rows.map(val => val.id);
    const deleteIdList = _this.flatData
      .filter(val => !contactIdList.includes(val.id))
      .map(val => val.id);
    const params = {
      tableType: 'menu',
      roleId: _this.nowRole.id,
      contactIdList,
      deleteIdList,
    }
    const [err] = await api_batchSynchronization(params);
    if (err) return;
    _this.initData();
  }
  /**
   * 判断行是否可以移动
   * @param row 当前行
   * @param direction 移动方向，'up'表示向上移动，'down'表示向下移动
   * @returns 是否可以移动
   */
  function canMove(row, direction) {
    const siblings = findSiblings(row, _this.tableData);
    if (!siblings) {
      return false;
    }
    const currentIndex = siblings.findIndex(item => item.id === row.id);
    return direction === 'up' ? currentIndex !== 0 : currentIndex !== siblings.length - 1;
  }
  /**
  * @description: 移动行的顺序
  * @param row 当前行
  * @param direction 移动方向，'up'表示向上移动，'down'表示向下移动
  */
  async function moveRow(row, direction) {
    if (!canMove(row, direction)) {
      return;
    }
    const siblings = findSiblings(row, _this.tableData);
    const currentIndex = siblings.findIndex(item => item.id === row.id);
    const targetRow = siblings[currentIndex + (direction === 'down' ? 1 : -1)];
    const targetId = targetRow.id;
    const [err,] = await api_modifyOrder({ id1: row.id, id2: targetId });
    if (err) {
      return;
    }
    ElMessage.success('移动成功');
    _this.initData();
  }
  /**
   * @description: 查找点击项的兄弟
   * @param row：点击项
   * @param nodes：被查询的树形结构数据
   * @returns 兄弟数组
   */
  function findSiblings(row, nodes) {
    for (const node of nodes) {
      if (node.children && node.children.length > 0) {
        const siblings = findSiblings(row, node.children);
        if (siblings) {
          return siblings;
        }
      }
      if (node.id !== row.id && node.parent === row.parent) {
        return nodes;
      }
    }
    return null;
  }
  return {
    selectMenu,
    showConfig,

    dialogMenuType,
    dialogMenuNeed,
    addMenu,
    modifyMenu,
    deleteMenu,
    select,
    //移动顺序
    ...{ moveRow, canMove }
  }
}