<template>
  <div class="space-between page-login">
    <div class="left">
    </div>
    <div class="right">
      <h1 class="title">后台管理系统</h1>
      <SignIn />
    </div>
  </div>
</template>

<script lang="ts">
import SignIn from './components/sign-in/index.vue'
export default {
  components: {
    SignIn,
  },
}
</script>

<style lang="scss" scoped>
.page-login{
  display: flex;
  .left, .right{
    height: 100vh;
  }

  $rightWidth: 490px;
  .left{
    width: calc(100% - $rightWidth);
    overflow: hidden;
    position: relative;
    > canvas{
      width: 100%;
      height: 100%;
      transform: scale(1.8);
    }
  }
  .right{
    width: $rightWidth;
    padding: 0 83px;
    padding-top: 20vh;
    box-sizing: border-box;
    position: relative;
    .title{
      text-align: center;
      margin-bottom: 14px;
      font-size: 27px;
      // letter-spacing: 1px;
    }
  }


}

</style>