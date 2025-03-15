import { defineStore } from "pinia";
import { api_getMenuList } from "../api/permissions";
import { routesAll } from "../router/create-routes";
import { RouteRecordRaw } from "vue-router";
import { deepClone, dataToTree } from "@/utils/object";
const newRoutes = deepClone(routesAll);  // 防止影响原数据

type TreeItem = {
  name: string
  id: string
  title: string
  parent: string
  children: TreeItem[]
}

export default defineStore({
  id: 'permissions',

  state: () => ({
    originList: [],  // 从后端获取的（具有权限）原数据
    routerList: [],  // 处理后的树形 router 数据
  }),

  actions: {
    /**
     * @description: 获取并匹配路由数据
     */
    async getMenuList(roleId: string | number) {
      const [err, res] = await api_getMenuList({ roleId })
      if (err) return;
      const originList = res.data.filter(val => val.selected);
      const tree = dataToTree(originList);
      const a = recursion(tree);
      console.log(a)
    },

    /**
     * 获取匹配路由
     * @param name 路由 name
     * @returns 
     */
    matched(name: string) {
      return getRouteMatched(this.routerList, name);
    }
  }
})

/**
 * 递归找到与后端匹配的路由
 * @param tree 处理后的树形结构数据
 * @returns
 */
function recursion(tree: TreeItem[]): RouteRecordRaw[] {
  const collect = [];
  tree.forEach((val, index) => {
    const route = newRoutes.find(item => val.name === item.name);
    if (route && val.children && val.children.length > 0) {
      route.children = recursion(val.children);
    }

    if (route) {
      route.children ??= [];
      collect.push(route);
    } else {
      // 本地压根儿没有的页面，重定向到 404
      const defaultRoute: RouteRecordRaw = {
        name: val.name,
        path: '/' + val.name.toLowerCase(),
        meta: { title: val.title },
        redirect: '/404',
      };
      collect.push(defaultRoute);
    }
  })
  return collect;
}

/**
 * 获取匹配路由
 * @param routes 路由数据
 * @param name 查找的 name
 * @param collect 无需传递，递归用
 * @returns 
 */
function getRouteMatched(routes: RouteRecordRaw[], name: string, collect: RouteRecordRaw[] = []) {
  for (let i = 0; i < routes.length; i++) {
    if (routes[i].name === name) {
      collect.push(routes[i]);
      break;
    }
    if (routes[i].children && routes[i].children.length > 0) {
      const results = getRouteMatched(routes[i].children, name, collect);
      if (results.length === 0) {
        continue;
      }
      collect.unshift(routes[i]);
    }
  }
  return collect;
}
