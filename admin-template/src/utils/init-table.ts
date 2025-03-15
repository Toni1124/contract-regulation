import { reactive, Ref, ref, watch } from "vue";
import { asyncto } from "./network";
import { pagingIndex } from "./number";
import { deleteEmpty } from "./object";
import { AnyObj } from "./type";

type RequestFn = (...args: any[]) => Promise<any[]>


/**
 * 初始化表格数据（含分页）
 * @note 包含了 搜索 与 分页 之间的逻辑
 * @note 如有特殊需求可进行继承 重写/追加
 */
export class InitTable<S extends object, C = RequestFn> {
  #initialForm: AnyObj  = {}
  #requestFn: RequestFn

  /**
   * @param searchForm 搜索条件，传入一个对象
   * @param requestFn  请求函数
   */
  constructor(searchForm: S, requestFn: RequestFn = () => asyncto(Promise.resolve())) {
    this.#initialForm = Object.freeze(searchForm);
    this.form         = reactive(Object.assign({}, this.#initialForm)) as S;

    this.#requestFn = requestFn;
  }


  // #region 分页
  paging = reactive({
    pageNumber: 1,
    pageSize:   10,
    total:      0,
  })

  /**
   * 改变页码
   * @param val 
   */
  onCurrentChange = (val: number) => {
    this.paging.pageNumber = val;
    this.initData();
  }

  /**
   * 改变单页数量
   * @param val 
   */
  onSizeChange = (val: number) => {
    this.paging.pageSize = val;
    this.initData();
  }

  /**
   * 分页索引计算
   */
  pagingIndex = (index: number) => {
    return pagingIndex(this.paging.pageNumber, this.paging.pageSize, index);
  }
  // #endregion


  // #region 搜索
  form: S  // 搜索条件

  /**
   * 搜索
   */
  search = () => {
    this.paging.pageNumber = 1;
    Promise.resolve().then(this.initData);
  }

  /**
   * 重置搜索
   */
  reset = () => {
    for (const key in this.#initialForm) {
      this.form[key] = this.#initialForm[key];
    }
    this.search();
  }
  // #endregion


  // #region 表格数据
  tableData: Ref<C[]> = ref([]);
  /**
   * 初始化数据
   */
  initData = async() => {
    const params = deleteEmpty({
      ...this.form,
      currentPage: this.paging.pageNumber,
      pageSize:    this.paging.pageSize,
    })
    

    const [err, res] = await this.#requestFn(params);
    if (err) {
      this.tableData.value = [];
      this.paging.total    = 0;
      return;
    }

    const { data, totalCount } = res.data;
    this.tableData.value = data;
    this.paging.total    = totalCount;
  }
  // #endregion

}



/**
 * 初始化表格数据（不分页）
 */
export class InitTableNoPaging<S extends object, C = any> extends InitTable<S, C> {
  #requestFn = null;

  /**
   * @param searchForm 搜索条件，传入一个对象
   * @param requestFn  请求函数
   */
  constructor(searchForm: S, requestFn: RequestFn) {
    super(searchForm, requestFn)
    this.#requestFn = requestFn;
  }

  initData = async () => {
    const params = deleteEmpty(this.form);
    const [err, res] = await this.#requestFn(params);
    if (err) {
      this.tableData.value = [];
      this.paging.total    = 0;
      return;
    }

    this.tableData.value = res.data;
    this.paging.total = res.data.length;
  }
}



// -------------------------------------------------------------------------------------------------


// 关于弹窗中的表格 下面的两个类（只考虑到较为简单的情况，较为复杂的页面还请直接继承 InitTable 这个类）

/**
 * 初始化表格数据（弹窗中的表格，含分页）
 * @note 多添加了一个控制弹窗的属性 visible
 */
export class InitTableDialog<S extends object, C = any> extends InitTable<S, C> {

  visible = ref(false);

  /**
   * @param searchForm 搜索条件，传入一个对象
   * @param requestFn  请求函数
   */
  constructor(searchForm: S, requestFn: RequestFn) {
    super(searchForm, requestFn);
    this.#watchVisible();
  }

  /**
   * 监听 visible 变化
   */
  #watchVisible = () => {
    watchVisibleSignUp.call(this);
  }
}



/**
 * 初始化表格数据（弹窗中的表格，不分页）
 * @note 多添加了一个控制弹窗的属性 visible
 */
export class InitTableDialogNoPaging<S extends object, C = any> extends InitTableNoPaging<S, C> {

  visible = ref(false);

  /**
   * @param searchForm 搜索条件，传入一个对象
   * @param requestFn  请求函数
   */
  constructor(searchForm: S, requestFn: RequestFn) {
    super(searchForm, requestFn);
    this.#watchVisible();
  }

  /**
   * 监听 visible 变化
   */
  #watchVisible = () => {
    watchVisibleSignUp.call(this);
  }
}


/**
 * 监听弹窗显示，初始化数据
 */
function watchVisibleSignUp() {
  watch(() => this.visible.value, value => {
    if (value) {
      this.initData();
    } else {
      this.tableData.value = [];
    }
  })
}
