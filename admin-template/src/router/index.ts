import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';
import { layoutRoutes } from './create-routes';
import env from '~/env';

// 添加调试代码
console.log('Generated Routes:', layoutRoutes);

const routes: Readonly<RouteRecordRaw[]> = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/login/index.vue')
  },
  {
    path: '/',
    name: 'Layout',
    component: () => import('../layout/index.vue'),
    children: layoutRoutes,  // 只使用自动生成的路由
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('../components/not-found/index.vue'),
  }
]

const router = createRouter({
  history: createWebHistory(env.BASE_URL),
  routes: routes,
})

// 添加导航守卫调试
router.beforeEach((to, from, next) => {
  console.log('Navigating to:', to.path);
  next();
});

export default router
