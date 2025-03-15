<template>
  <main ref="container" class="layout-container">
    <div ref="header">
      <slot name="header" />
    </div>
    <div :style="{ height: height + 'px' }">
      <slot />
    </div>
    <div ref="footer" class="paging" >
      <slot name="footer" />
    </div>
  </main>
</template>

<script lang="ts">
import { onMounted, getCurrentInstance, ref } from 'vue';

/**
 * 管理端每个页面的容器
 */
export default {
  props: {
    mainHeight: {
      type: Number,
      default: 0,
    },
  },
  setup() {
    const current = getCurrentInstance();

    const height = ref(0);

    onMounted(() => {
      const elContainer = current.refs.container as HTMLElement;
      const elHeader = current.refs.header as HTMLElement;
      const elFooter = current.refs.footer as HTMLElement;
      
      height.value = elContainer.offsetHeight - elHeader.offsetHeight - elFooter.offsetHeight - 30;
    })

    return {
      height
    }
  }
}
</script>

<style lang="scss">
.layout-container{
  margin: 14px;
  margin-top: 0;
  padding: 14px 15px;
  border-radius: 4px;
  background: white;
  height: calc(100vh - 150px);
  .paging{
    padding: 5px 0;
    box-sizing: border-box;
  }
}
</style>

