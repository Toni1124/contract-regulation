<template>
  <el-menu
    :default-active="activeMenu"
    :collapse="isCollapse"
    :unique-opened="false"
    :collapse-transition="false"
    class="el-menu-vertical"
    @select="handleSelect"
  >
    <template v-for="route in routes" :key="route.path">
      <el-menu-item v-if="!route.children" :index="route.path">
        <el-icon v-if="route.meta?.icon">
          <component :is="'Icon' + route.meta.icon" />
        </el-icon>
        <template #title>{{ route.meta?.title }}</template>
      </el-menu-item>

      <el-sub-menu v-else :index="route.path">
        <template #title>
          <el-icon v-if="route.meta?.icon">
            <component :is="'Icon' + route.meta.icon" />
          </el-icon>
          <span>{{ route.meta?.title }}</span>
        </template>
        
        <el-menu-item 
          v-for="child in route.children"
          :key="child.path"
          :index="child.path"
        >
          <el-icon v-if="child.meta?.icon">
            <component :is="'Icon' + child.meta.icon" />
          </el-icon>
          <template #title>{{ child.meta?.title }}</template>
        </el-menu-item>
      </el-sub-menu>
    </template>
  </el-menu>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Setting } from '@element-plus/icons-vue'
import { layoutRoutes } from '@/router/create-routes'
import { getSlidebarMenus } from '@/layout/slidebar'

const route = useRoute()
const router = useRouter()

const isCollapse = ref(false)
const routes = computed(() => getSlidebarMenus(layoutRoutes))
const activeMenu = computed(() => route.path)

const handleSelect = (path: string) => {
  router.push(path)
}
</script>

<style lang="scss" scoped>
.el-menu-vertical {
  height: 100%;
  border-right: none;
}

:deep(.el-sub-menu .el-sub-menu__title) {
  padding-left: 20px !important;
}

:deep(.el-menu-item) {
  padding-left: 20px !important;
}

.el-menu--collapse {
  :deep(.el-sub-menu) {
    .el-sub-menu__title {
      padding-left: 20px !important;
    }
  }
}
</style> 