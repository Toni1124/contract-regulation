import useStoreTabs from '@/store/tabs';
import { useRoute } from 'vue-router';
import useStoreSlider from '@/store/slidebar';
import { computed } from 'vue';

export default () => {
  const stoteTabs = useStoreTabs();

  const route = useRoute();
  stoteTabs.add(route.path, route.meta.title as string, route.name as string);

  const storeSlider = useStoreSlider()
  const shrink = computed(() => !storeSlider.unfold);

  return {
    shrink,
  }
}
