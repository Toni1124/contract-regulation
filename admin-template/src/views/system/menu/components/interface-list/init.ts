import { InitTable } from "@/utils/init-table";
import { deleteEmpty } from "@/utils/object";
import { api_getInterfaceList } from "@/api/permissions";
import { getCurrentInstance, nextTick } from "vue";

const searchForm = {
  url: '',
}

export class Init extends InitTable<typeof searchForm> {
  #current = null;
  #props   = null;

  constructor() {
    super(searchForm, api_getInterfaceList);
    this.#current = getCurrentInstance();
    this.#props   = this.#current.props;
  }

  initData = async () => {
    const params = deleteEmpty({
      roleId: this.#props.roleId,
      menuId: this.#props.menuId,
      ...this.form,
    })
    const [err, res] = await api_getInterfaceList(params);
    if (err) return;
    this.tableData.value = res.data;

    const tableEl: any = this.#current.refs.tableEl;
    const selectList = res.data.filter(val => val.selected);
    nextTick(() => {
      selectList.forEach(val => tableEl.toggleRowSelection(val));
    })
  };

}