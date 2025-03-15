<template>
  <div class="mouse-wheel-horizontal-scroll">
    <div class="mouse-wheel-wrapper" ref="scroll">
      <div class="mouse-wheel-content">
        <slot />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import BScroll from '@better-scroll/core'
import MouseWheel from '@better-scroll/mouse-wheel'
import { onMounted, getCurrentInstance } from 'vue'

BScroll.use(MouseWheel)

/**
 * 可横向拖拽的容器
 */
export default {
  setup() {
    const current = getCurrentInstance();
    let scroll = null;
    onMounted(() => {
      scroll = new BScroll(current.refs.scroll as HTMLElement, {
        scrollX: true,
        scrollY: false,
        mouseWheel: true
      })
    })

    function refresh() {
      scroll.refresh()
    }

    return {
      refresh
    }
  }
}
</script>

<style lang="scss">
.mouse-wheel-horizontal-scroll{
  .mouse-wheel-wrapper{
    white-space: nowrap;
    overflow: hidden;
    .mouse-wheel-content{
      display: inline-block;
    }
  }
}
</style>