export type RouteConfig = {
  [K: string]: {
    order?:    number
    title:     string
    icon?:     string
    redirect?: string                  // name | path
    hidden?:   boolean                 // 在侧边栏隐藏
    roles?:    Array<string | number>  // 授权角色
    dynamic?:  string                  // 动态路由页面
    href?:     string                  // 外部链接
  }
}

export const exclude = ['login'];  // 排除页面，不参与生成路由

// key 对应 @/src/views/<url> 转大驼峰
export const pageConfig: RouteConfig = {
  BlackWhiteList: {
    order: 1,  // 添加顺序，数字越小越靠前
    icon: '&#xe004;',
    title: '黑白名单管理',
  },
  ContractAudit: {  // 确保这个名字和 views 目录下的文件夹名称完全一致
    order: 2,
    icon: '&#xe004;',
    title: '智能合约审核',
  },
  RuleManagement: {
    order: 3,  // 添加顺序，数字越小越靠前
    icon: '&#xe004;',
    title: '监管规则配置',
  },
  RuleManagementEdit: {
    title: '编辑规则',
    hidden: true,  // 在菜单中隐藏
  },
  RuleManagementContract: {
    title: '合约详情',
    hidden: true,
  },
  Example:
    { icon: '&#xe004;', title: '例子', },
  ExampleTable:
    { title: '表格', },
  ExampleChild2:
    { title: '二级菜单', },
  ExampleChild2Grandson1:
    { title: '三级菜单1', },
  ExampleChild2Grandson2:
    { title: '三级菜单2', },
  ExampleDynamic:
    { title: '动态路由页', dynamic: ':id', hidden: true },
  System:
    { icon: '&#xe004;', title: '系统管理', },
  SystemRoles:
    { title: '角色管理', },
  SystemMenu:
    { title: '权限分配', },
}
