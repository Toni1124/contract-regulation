import { defineStore } from "pinia";

export default defineStore({
  id: 'slidebar',

  state: () => ({
    unfold: true,
  }),

  actions: {
    open(bool: boolean) {
      this.unfold = bool;
    }
  }
})