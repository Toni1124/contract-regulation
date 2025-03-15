import { getCurrentInstance, nextTick, provide, reactive, ref, watch } from "vue"
import { dataToTree, deleteEmpty } from "@/utils/object";
import { api_getRoleList, api_getMenuList } from '@/api/permissions';
import { InitTable } from "@/utils/init-table";


const searchForm = {
  name: '',
  title: '',
}

export default class extends InitTable<typeof searchForm> {

  #current = null;

  nowRole = reactive({ role: '', id: '' });
  roleList = ref([]);
  getRoleList = async () => {
    const [err, res] = await api_getRoleList({});
    if (err) return false;

    const list = dataToTree(res.data);
    if (list.length === 0) return false;

    this.roleList.value = list;
    if (list.length > 0) {
      this.nowRole.role = list[0].role;
      this.nowRole.id = list[0].id;
    }
    return true;
  }

  constructor() {
    super(searchForm, api_getMenuList);
    this.#current = getCurrentInstance();

    this.getRoleList();
    watch(() => this.nowRole.id, value => {
      this.initData();
    })

    provide('getRoleList', () => this.roleList.value);
    provide('getMenuList', () => this.tableData.value);
  }

  treeNodeClick = (row) => {
    this.nowRole.id = row.id;
  }

  flatData = ref([]);  // 原始数据
  initData = async () => {
    if (this.roleList.value.length === 0) {  // 保证角色获取成功
      const result = await this.getRoleList();
      if (!result) return;
    }
    const params = deleteEmpty({
      roleId: this.nowRole.id,
      ...this.form,
    })
    const [err, res] = await api_getMenuList(params);
    if (err) return;

    const data = res.data;
    const list: any[] = dataToTree(data);
    this.flatData.value = data;
    this.tableData.value = list;

    nextTick(() => {
      const tableEl: any = this.#current.refs.tableEl;
      recursionSelected(this.tableData.value, tableEl);
    })
  };

}

/**
 * 递归选择
 * @param list 
 * @param tableEl 
 */
function recursionSelected(list: any[], tableEl) {
  list.forEach(val => {
    tableEl.toggleRowSelection(val, val.selected);
    if (val.children && val.children.length > 0) {
      val.children.map(item => {
        recursionSelected(val.children, tableEl)
      })
    }
  });
}
