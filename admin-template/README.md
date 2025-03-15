# 后台管理系统

## 自动生成页面

1. 管理端系统有着一定规则的业务系统，强烈建议使用脚手架导入统一处理；
  - 避免出现不必要的错误。
2. 不想参与生成路由的页面可通过 src/router/config.ts `exclude` 进行排除；
3. 页面组件 components 文件夹不会参与路由生成。

## 账号密码

- 随便输

## 接口返回形式

- 该框架将请求一律以 [err, res] 形式返回数据，因为大部分开发者经常忘记 `.catch()`

## 页面缓存功能

- 将页面组件的 name 设置为：相对路径转大驼峰形式，（如： src/views/example/table/index.vue -- ExampleTable）

## 组件 props 重置

- src/utils/element-reset.ts

## 表格搜索/分页 逻辑

- 一律使用 src/utils/init-table.ts 中的 `InitTable` 继承

## 角色管理 & 权限分配

- 后端代码： https://github.com/yubo9807/go_power
