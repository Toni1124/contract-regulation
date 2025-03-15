/**
 * vue3 KeepAlive 使用方式有变动
 * https://v3.cn.vuejs.org/api/built-in-components.html#keep-alive
 */
<template>
  <router-view v-slot="row">
    <keep-alive :include="tabs">
      <component :is="row.Component" />
    </keep-alive>
  </router-view>
</template>

<script lang="ts">
import { computed } from 'vue';
import useStoreTabs from '@/store/tabs';

/**
 * 页面缓存控制
 * @props include
 */
export default {
  setup() {
    const storeTabs = useStoreTabs();
    const tabs = computed(() => storeTabs.exclude.concat(storeTabs.list).map(val => val.name));
    return {
      tabs
    }
  }
}

</script>
