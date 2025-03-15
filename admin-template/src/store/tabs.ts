import { defineStore } from "pinia";
import type { Router } from "vue-router";

export type TabItem = {
  name: string
  title: string
  path: string
}
type State = {
  exclude: TabItem[]  // 不可关闭项
  list: TabItem[]
}

export default defineStore({
  id: 'tabs',

  state: (): State => ({
    exclude: [],
    list: [],
  }),

  actions: {

    /**
     * 获取缓存的 name
     * @param this 
     * @returns 
     */
    getCaches(this: State) {
      return this.list.filter(val => val.name).map(val => val.name);
    },

    /**
     * 添加
     * @param name 
     */
    add(path: string, title: string, name?: string) {
      if (this.exclude.find(val => val.path === path)) return;

      const index = this.list.findIndex(val => val.path === path);
      if (index >= 0) return;
      this.list.push({ name, title, path });
    },

    /**
     * 删除
     * @param key
     */
    del(path: string) {
      const index = this.list.findIndex(val => val.path === path);
      if (index >= 0) {
        this.list.splice(index, 1);
      }
    },

    /**
     * 清空全部
     */
    clearAll() {
      this.list = [];
    },

    /**
     * 关闭当前页
     * @param router 
     */
    close(router: Router) {
      this.del(router.currentRoute.value.path);
      const len = this.list.length;
      if (len > 0) {
        router.push({ path: this.list[len - 1].path });
      }
    },
  }

})
