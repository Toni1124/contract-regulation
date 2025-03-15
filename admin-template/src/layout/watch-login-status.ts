import useStoreUser from '../store/user';
import { computed, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';

export default () => {
  const $router = useRouter();
  const $route  = useRoute();

  const storeUser = useStoreUser();

  const login = computed(() => storeUser.login);

  // 监听登录状态，退出页面
  watch(() => login.value, value => {
    if (value === 1) return;
    exitLayout();
  })
  
  /**
   * 退出
   */
  function exitLayout() {
    const redirectHref = $route.path;
    $router.replace(`/login?redirect=${redirectHref}`);
    storeUser.signOut();
  }

  return {}
}