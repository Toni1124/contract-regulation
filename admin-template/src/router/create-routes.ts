import { createNum } from "@/utils/number";
import { toGreatHump } from "@/utils/string";
import { RouteRecordRaw } from "vue-router";
import { pageConfig } from "./config";
import { AnyObj } from "@/utils/type";

const exclude = ['login'];  // 排除页面，不参与生成路由

const iter = createNum();
const order = () => iter.next().value as number;

/**
 * name 转 path
 * @param name 
 * @returns 
 */
function nameToPath(name: string) {
  if (name.startsWith('/')) return name;
  const arr = name.split('');
  let path = '';
  arr.forEach(val => {
    if (/[A-Z]/.test(val)) {
      path += '/' + val.toLowerCase();
    } else {
      path += val;
    }
  })
  return path;
}

/**
 * 获取所有 routes
 * @returns 
 */
function getRoutesAll(): RouteRecordRaw[] {  
  const obj = import.meta.glob('../views/**/index.vue');  // vite

  const routes = [];
  for (const prop in pageConfig) {
    const item = pageConfig[prop];
    item.order = order();
    if (item.href) {
      routes.push({
        path: item.href,
        meta: item,
      })
    }
  }

  for (const prop in obj) {
    let isExclude = false;
    exclude.forEach(val => prop.includes(val) && (isExclude = true));
    if (isExclude || prop.includes('/components/')) continue;

    const splits = prop.split('/');
    const arr = splits.slice(2, splits.length - 1);

    const name = arr.map(val => toGreatHump(val)).join('');
    const item = pageConfig[name];
    if (!item) continue;

    const redirect = item && item.redirect;
    let path = '/'+arr.join('/');
    if (item.dynamic) {
      path += '/' + item.dynamic;
    }
    const config: AnyObj = {
      path,
      component: obj[prop],
      meta: item,
      redirect: redirect && nameToPath(redirect),
    }
    if (!item.dynamic) config.name = name;
    routes.push(config);
  }

  return routes.sort((a, b) => a.meta.order - b.meta.order);
}

export const routesAll = getRoutesAll();

/**
 * 获取树形结构 routes
 * @param routes 
 * @returns 
 */
function getTreeRoutes(routes: RouteRecordRaw[]) {
  const indexArr = [];
  const newRoutes = [];
  routes.forEach((val, i) => {
    const children = routes.filter((item, j) => {
      const bool = item.path.startsWith(val.path + '/');
      bool && indexArr.push(j);
      return bool;
    });
    if (children.length > 0) {
      val.redirect ??= children[0].path;  // 没有设置重定向，但又是个目录
      val.children = getTreeRoutes(children);
    }
    !indexArr.includes(i) && newRoutes.push(val);
  })
  return newRoutes;
}

// 导出最终的路由配置
export const layoutRoutes = getTreeRoutes(routesAll);
