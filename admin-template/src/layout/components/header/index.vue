<template>
  <header class="header">
    <div class="left">
      <i class="iconfont icon" v-html="nowIcon"></i>
      <i class="iconfont icon">&#xe01b;</i>
      <el-breadcrumb>
        <el-breadcrumb-item v-for="(item, index) in breadcrumb" :key="index" :to="{ name: item.name }">{{
          item.title
        }}</el-breadcrumb-item>
      </el-breadcrumb>
    </div>

    <div class="right">
      <ul class="clearfix">
        <li class="user-name">
          <img class="portrait" src="" alt="">
          {{ userInfo.username }}
          <el-dropdown>
            <i class="iconfont">&#xe00c;</i>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="signOut">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </li>
        <!-- <li>
          <i>icon</i>
          消息通知
        </li> -->
      </ul>
    </div>

  </header>
</template>

<script lang='ts'>
import { defineComponent } from 'vue';
import user from './user';
import breadcrumb from './breadcrumb';

export default defineComponent({
  setup() {
    return {
      ...user(),
      ...breadcrumb(),
    }
  }
})
</script>

<style lang='scss' scoped>
.header {
  display: flex;
  justify-content: space-between;
  padding: 14px 10px 4px;
}

$logoWidth: 120px;

.left {
  margin-top: 6px;

  .icon {
    margin-right: 6px;
    vertical-align: middle;
  }

  .el-breadcrumb {
    display: inline-block;
    vertical-align: middle;
    margin-top: 2px;
  }

  :deep(.el-breadcrumb__item .el-breadcrumb__inner) {
    padding: 5px 14px;
    border-radius: 4px;
    font-weight: 700;
  }

  :deep(.el-breadcrumb__item:first-child .el-breadcrumb__inner) {
    padding-left: 0;
    padding-right: 0;
  }

  :deep(.el-breadcrumb__item:not(:first-child) .el-breadcrumb__inner) {
    color: #E58F46;
    background: #E58F4620;
  }
}


$accountWidth: 270px;

.right {
  width: $accountWidth;

  >ul {
    >li {
      float: right;
      line-height: 44px;

      &:not(:last-child) {
        margin-left: 24px;
      }

      &.user-name {
        font-weight: 700;
      }
    }
  }

  .portrait {
    width: 44px;
    height: 44px;
    border-radius: 50%;
    overflow: hidden;
    vertical-align: middle;
    margin-right: 8px;
  }
}

.el-dropdown {
  cursor: pointer;
}
</style>