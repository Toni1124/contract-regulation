import { createApp } from "vue";
import { createPinia } from "pinia";
import router from "./router";

import ElementPlus from 'element-plus'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import 'element-plus/dist/index.css'
import * as icons from '@element-plus/icons-vue'
import './utils/element-reset'
import { Setting } from '@element-plus/icons-vue'

import './styles/index.scss';
import App from "./App.vue";
import './right-control'

import LayoutContainer from './components/layout-container/index.vue'
import LayoutSearch from './components/layout-search-header/index.vue';
import RouteCache from '@/components/route-cache/index.vue'

const app = createApp(App);
app
  .use(router)
  .use(createPinia())
  .use(ElementPlus, { locale: zhCn })
  .mount("#app");

for (const name in icons) {
  app.component('Icon' + name, icons[name])
}
app.component('RouteCache', RouteCache)
app.component('LayoutContainer', LayoutContainer)
app.component('LayoutSearch', LayoutSearch)
app.component('Setting', Setting)

