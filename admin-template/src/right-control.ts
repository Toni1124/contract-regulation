import { getToken } from '@/utils/auth';
import router from './router';
import { layoutRoutes, routesAll } from './router/create-routes';
import useStoreUser from './store/user';
import useStorePermissions from './store/permissions';

Promise.resolve().then(() => {
  const storeUser = useStoreUser();
  const storePermissions = useStorePermissions();
  let lock = true;
  router.beforeEach(async(to, from, next) => {

    // 退出登录把锁打开，再次进入保证重新获取用户数据
    if (storeUser.login === 2) lock = true;

    if (to.name === 'Login' && getToken()) {
      const name = getHomeRoute(storeUser.role).name;
      router.replace({ name });
      return next();
    }

    // 不属于 layout
    if (to.matched[0].name != 'Layout') return next();

    // 没有登录
    if (!getToken()) {
      router.replace('/login');
      return next();
    }

    // 获取用户信息，保证进入页面只请求一次
    if (lock) {
      await storeUser.getUserInfo();
      if (storeUser.login !== 1) {
        router.replace('/login');
        return next();
      }
      // await storePermissions.getMenuList(0);
    }
    lock = false;

    // Layout 没有指定首页
    const isExist = routesAll.some(val => val.name === to.name);
    if (!isExist) {
      const name = getHomeRoute(storeUser.role).name;
      router.replace({ name });
      return next();
    }

    // 没有设置权限，相当于设置了所有权限
    // 这里的 to.meta 会继承父级的属性，不晓得为啥子
    const roles = to.matched[to.matched.length-1].meta.roles;
    if (!roles) return next();

    // 符合设置权限
    const bool = (roles as (number | string)[]).includes(storeUser.role);
    if (bool) return next();

    // 权限不符合，跳转到首页
    const name = getHomeRoute(storeUser.role).name;
    router.replace({ name });
    next();
  })
})



/**
 * 获取可作为首页的 route
 * @param route 目标 route
 * @param role  角色
 * @returns 
 */
function getHomeRoute(role: string | number) {
  const len = layoutRoutes.length
  let queryIndex = 0;

  for (let i = 0; i < len; i++) {
    const newRoute = layoutRoutes[i];
    const roles = newRoute.meta.roles as (string | number)[];

    // 1. 没有设置过权限，可以作为首页
    if (!roles) {
      queryIndex = i;
      break;
    };

    // 2. 设置了权限，但权限不对
    if (!roles.includes(role)) {
      if (i === len - 1) {  // 已经是最后一个，但权限还是不对
        queryIndex = -1;
      }
      continue;  // 看下一个是否符合
    }

    queryIndex = i;
    break;
  }

  // 没有找到任何可用页面
  if (queryIndex < 0) {
    const NotFoundRoute = router.options.routes.find(val => val.name === 'NotFound');
    return NotFoundRoute;
  }

  return layoutRoutes[queryIndex];
}
