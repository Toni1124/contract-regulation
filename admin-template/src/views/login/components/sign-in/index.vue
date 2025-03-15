<template>
  <el-form ref="formRef" :model="form" :rules="rules" class="login" label-width="60px" label-position="top">
    <el-form-item label="账号" prop="username">
      <el-input v-model="form.username" placeholder="请输入账号" :clearable="false">
        <template #prefix>
          <i class="iconfont">&#xe028;</i>
        </template>
      </el-input>
    </el-form-item>
    <el-form-item label="密码" prop="password">
      <el-input v-model="form.password" placeholder="请输入密码" :clearable="false" :type="exposePassword ? 'text' : 'password'">
        <template #prefix>
          <i class="iconfont">&#xe027;</i>
        </template>
        <template #suffix>
          <i v-show="!exposePassword" class="iconfont" @click="exposePassword = !exposePassword">&#xe026;</i>
          <i v-show="exposePassword" class="iconfont" @click="exposePassword = !exposePassword">&#xe024;</i>
        </template>
      </el-input>
    </el-form-item>
    <el-form-item label="验证码" prop="code">
      <el-input v-model="form.code" placeholder="请输入验证码" :clearable="false" @keyup.enter="signIn">
        <template #prefix>
          <i class="iconfont">&#xe025;</i>
        </template>
        <template #suffix>
          <img :src="form.captcha" alt="验证码" height="40" @click="getCaptcha">
        </template>
      </el-input>
    </el-form-item>
    <el-button type="primary" class="sign-in-button" @click="signIn">登录</el-button>
  </el-form>
</template>

<script lang="ts">
import { ref } from 'vue';
import form from './form';

export default {
  setup() {
    const exposePassword = ref(false);
    return {
      ...form(),
      exposePassword,
    }
  }
}
</script>

<style lang="scss" scoped>
.login{
  position: relative;
  height: 70vh;
  :deep(.el-input__inner), :deep(.el-button){
    height: 48px;
  }
  :deep(.el-input__wrapper){
    border-radius: 0;
    input::placeholder{
      color: var(--main-font-color);
    }
  }
  .sign-in-button{
    position: absolute;
    bottom: 30px;
    width: 100%;
    background: var(--main-color);
  }
}
</style>