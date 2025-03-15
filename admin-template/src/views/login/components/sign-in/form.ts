import { api_getCaptcha, api_signIn } from '@/api/login';
import { reactive } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import useStoreUser from '@/store/user';
import { ElForm } from 'element-plus'
import { useCompRef } from '@/utils/type';
import { DEVELOPMENT } from '~/env';

export default () => {

  const $route    = useRoute();
  const $router   = useRouter();
  const storeUser = useStoreUser();

  const isDev = DEVELOPMENT === 'development';
  const form = reactive({
    username: isDev ? 'admin' : '',
    password: isDev ? 'admin' : '',
    captcha: '',
    code: '',
    uuid: '',
  })
  const rules = {
    username: { required: true, message: '请输入用户名', trigger: 'blur' },
    password: { required: true, message: '请输入密码', trigger: 'blur' },
    code: { required: true, message: '请输入验证码', trigger: 'blur' },
  }

  const formRef = useCompRef(ElForm);

  getCaptcha();
  /**
   * 获取验证码
   */
  async function getCaptcha() {
    const [err, res] = await api_getCaptcha();
    if (err) return;

    const { imageBase64, uuid } = res.data;
    form.captcha = 'data:image/png;base64,' + imageBase64;
    form.uuid = uuid;
  }

  /**
   * 登录
   */
  async function signIn() {
    formRef.value.validate(async valid => {
      if (!valid) return;

      const [err, res] = await api_signIn({
        username: form.username,
        password: form.password,
        code: form.code,
        uuid: form.uuid,
      });
      if (err) return;

      storeUser.signIn(res.data.tokenValue);
      const redirect = $route.query.redirect || '/';
      $router.replace((redirect as string));
    })
  }

  return {
    formRef,
    form,
    rules,
    getCaptcha,
    signIn,
  }
}