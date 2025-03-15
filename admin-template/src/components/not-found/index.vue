<template>
  <div class="page-not-found">
    <div class="text-404">404</div>
    <router-link to="/" replace>返回首页</router-link>
  </div>
</template>

<script lang="ts">
/**
 * 404 页面
 */
export default {}
</script>

<style lang="scss" scoped>
.page-not-found{
  margin-top: 200px;
  text-align: center;
  .text-404{
    font-weight: 900;
    color: var(--main-color);
    font-size: 100px;
  }
}
</style>