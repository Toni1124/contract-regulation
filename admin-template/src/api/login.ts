import { AnyObj } from '@/utils/type';
import request from './request';

/**
 * 获取验证码
 */
export function api_getCaptcha() {
  // return request({
  //   url: '/captcha',
  //   method: 'get',
  //   responseType: 'arraybuffer',
  // })
  return Promise.resolve(['auth code', null])
}

/**
 * 登录
 */
export function api_signIn(data: AnyObj) {
  // return request({
  //   url: '/login',
  //   method: 'post',
  //   data,
  // })
  return Promise.resolve([null, {
    code: 200,
    data: {
      token: 'to.ken.360',
    },
  }])
}

/**
 * 获取用户信息
 */
export function api_getUserInfo() {
  // return request({
  //   url: '/user/getUserInfo',
  //   method: 'get',
  // });
  return Promise.resolve([null, {
    code: 200,
    data: {
      username: 'admin',
      roles: [{ roleid: 1 }]
    }
  }])
}
