<template>
  <ul class="menu">
    <MenuItem v-for="(item, index) in navList" :key="index" :menu="item" :shrink="shrink" :nowRoutes="nowRoutes" />
  </ul>
</template>

<script lang="ts">
import MenuItem from './item.vue'
import nav from './nav';
import tabs from './tabs';

export default {
  components: {
    MenuItem,
  },
  setup() {
    return {
      ...nav(),
      ...tabs(),
    }
  }
}
</script>

<style lang="scss" scoped>
.menu{
  padding: 0 14px;
}
</style>