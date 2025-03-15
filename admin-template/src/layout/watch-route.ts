import { watch } from "vue"
import { useRoute } from "vue-router"
import useStoreTabs from '@/store/tabs';

export default () => {

  const route = useRoute();
  const storeTabs = useStoreTabs();

  // 路由发生变化
  watch(() => route.path, () => {
    route.matched.forEach((item, i) => {
      if (i === 0) return;
      const title = item.children.length > 0 ? null : item.meta.title as string;
      storeTabs.add(item.path, title, item.name as string);
    })
  }, { immediate: true })

  return {
  }
}