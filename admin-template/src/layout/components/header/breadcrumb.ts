import { ref, watch } from "vue";
import { useRoute } from "vue-router"

export default () => {
  const $route = useRoute();

  const nowIcon = ref('');
  const breadcrumb = ref([]);

  watch(() => $route.path, value => {
    getBreadcrumb();
  }, { immediate: true })

  function getBreadcrumb() {
    breadcrumb.value = [];
    $route.matched.forEach(val => {
      if (val.name === 'Layout') return;
      nowIcon.value = val.meta && val.meta.icon as string;
      breadcrumb.value.push({
        name: val.name,
        path: val.path,
        title: val.meta && val.meta.title,
      })
    })
  }

  return {
    nowIcon,
    breadcrumb,
  }
}
