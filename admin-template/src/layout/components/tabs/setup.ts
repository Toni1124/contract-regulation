import useStoreTabs, { TabItem } from '@/store/tabs';
import { ref, getCurrentInstance, nextTick, reactive, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';

export default () => {
  const router = useRouter();
  const storeTabs = useStoreTabs();
  const current = getCurrentInstance();

  const tabs = computed(() => {
    const exclude = storeTabs.exclude.map(val => ({ ...val, disable: true }));
    const list = storeTabs.list.map(val => ({ ...val, disable: false })).filter(val => val.title);
    nextTick(() => {
      (current.refs.mouseWheelX as any).refresh()
    })
    return exclude.concat(list);
  });

  function jump(path: string) {
    router.push({ path });
  }


  // #region 右键菜单
  let selectTab: TabItem = null;
  const visible = ref(false);
  const menuPosition = reactive({
    top: 0,
    left: 0,
  });

  /**
   * 右键菜单
   */
  function rightMenu(e: MouseEvent, item: TabItem) {
    e.preventDefault();
    selectTab = item;
    visible.value = true;
    menuPosition.top = e.clientY;
    menuPosition.left = e.clientX;
  }

  /**
   * 关闭指定tab
   */
  function close(path: string) {
    storeTabs.del(path);
    if (path === currentPath.value) {
      router.push({ path: tabs.value[tabs.value.length - 1].path });
    }
  }

  function closeOwn() {
    close(selectTab.path);
    visible.value = false;
  }

  /**
   * 关闭其他
   */
  function closeOther() {
    storeTabs.clearAll();
    storeTabs.add(selectTab.path, selectTab.title, selectTab.name);
    router.push({ path: selectTab.path });
    visible.value = false;
  }

  /**
   * 关闭全部
   */
  function closeAll() {
    storeTabs.clearAll();
    router.push('/');
    visible.value = false;
  }
  // #endregion


  const route = useRoute();
  const currentPath = computed(() => route.path);

  return {
    tabs,
    jump,
    close,
    closeOwn,
    closeOther,
    closeAll,

    visible,
    menuPosition,
    rightMenu,

    currentPath,
  }
}