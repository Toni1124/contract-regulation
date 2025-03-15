<template>
  <li :class="['tier-'+count, shrink && 'shrink']">
    <a v-if="menu.href" :href="menu.href" target="_blank">
      <div class="box">
        <i class="iconfont icon" v-html="menu.icon"></i>
        <span class="title">{{ menu.title }}</span>
      </div>
    </a>
    <router-link v-else :to="menu.path" :class="[isOpen && 'active']" v-slot="{ navigate }">
      <div class="box" @click.prevent="open(menu)">
        <i v-if="count === 0" class="iconfont icon" v-html="menu.icon"></i>
        <span class="title">{{ menu.title }}</span>
        <i v-show="menu.children && menu.children.length > 0" class="iconfont icon-open"><IconArrowRight/></i>
      </div>
    </router-link>

    <ul
      v-if="menu.children.length > 0"
      ref="menuRef"
      :class="['menu', isOpen && 'active']"
      :style="{ height }"
    >
      <MenuItem v-for="(item, index) in menu.children" :key="index" :menu="item" :shrink="shrink" :count="count+1" :nowRoutes="nowRoutes" />
    </ul>

  </li>
</template>

<script lang="ts">
import { ref, getCurrentInstance, PropType, nextTick } from 'vue'
import { useRouter } from 'vue-router';

type MenuType = {
  children: MenuType[],
  icon: string,
  title: string,
  name: string,
  path: string,
  href: string,
}

export default {
  name: 'MenuItem',
  props: {
    menu: {
      type: Object as PropType<MenuType>,
      default: () => ({}),
    },
    nowRoutes: {
      type: Array as PropType<string[]>,
      default: []
    },
    shrink: {
      type: Boolean,
      default: false,
    },
    /**
     * 组件递归计数，不需要传递
     */
    count: {
      type: Number,
      default: 0,
    },
  },
  setup(props) {
    const current = getCurrentInstance();
    const router = useRouter();


    if (props.nowRoutes.includes(props.menu.name)) {
      nextTick(() => open(props.menu));
    }

    const isOpen = ref(false);
    const height = ref('0');

    /**
     * 展开目录
     * @param row 
     */
    function open(row: MenuType) {
      if (row.children.length === 0) {  // 不是一个目录
        router.push({ name: row.name });
        return;
      }
      if (props.shrink) return;  // 菜单被收起

      const el = current.refs.menuRef as HTMLElement;
      if (isOpen.value) {  // 展开
        isOpen.value = false;
        el.style.height = 'auto';
        const h = el.offsetHeight;
        height.value = h + 'px';
        setTimeout(() => {
          height.value = '0';
        })
      } else {  // 收起
        isOpen.value = true;
        el.style.height = 'auto';
        const h = el.offsetHeight;
        el.style.height = '0';
        setTimeout(() => {
          height.value = h + 'px';
          setTimeout(() => {
            height.value = 'auto';
          }, 400)
        }, 0)
      }
    }

    return {
      isOpen,
      height,
      open,
    }
  }
}
</script>

<style lang="scss" scoped>
@use './item.scss';
</style>
