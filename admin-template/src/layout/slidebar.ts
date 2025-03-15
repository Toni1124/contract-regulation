import useStoreSlidebar from '@/store/slidebar';
import { computed } from 'vue';
import { RouteRecordRaw } from 'vue-router';

export default () => {
  const storeSlidebar = useStoreSlidebar();

  const unfold = computed(() => storeSlidebar.unfold);

  function open() {
    storeSlidebar.open(!unfold.value);
  }

  return {
    unfold,
    open,
  }
}

export function getSlidebarMenus(routes: RouteRecordRaw[]) {
  return routes
    .filter(route => {
      // 过滤不需要显示的路由
      return !route.meta?.hidden;
    })
    .sort((a, b) => {
      // 根据 sort 排序
      return (a.meta?.sort || 0) - (b.meta?.sort || 0);
    });
}