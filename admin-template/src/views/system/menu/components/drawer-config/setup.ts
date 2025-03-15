import { getCurrentInstance, nextTick, Ref, ref, watch } from "vue";

export default () => {

  const current = getCurrentInstance();

  const visible = ref(false);

  const selectType: Ref<0|1> = ref(0);  // 0: 接口  1: 元素

  const refConfig = {
    0: 'interfaceListRef',
    1: 'elementListRef',
  }

  watch(() => visible.value, value => {
    if (value) {
      nextTick(() => {
        const comp: any = current.refs[refConfig[selectType.value]];
        comp.initData();
      })
    }
  })

  watch(() => selectType.value, value => {
    const comp: any = current.refs[refConfig[value]];
    comp.initData();
  })

  return {
    visible,
    selectType
  }
}