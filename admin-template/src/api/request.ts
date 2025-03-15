import { AxiosResponse } from 'axios';
import { ElMessageBox } from 'element-plus';

import { asyncto, Request, SateConfig } from '@/utils/network';
import useStoreUser from '../store/user';
import { nextTick } from 'vue';

let storeUser = null;
nextTick(() => {
  storeUser = useStoreUser();
})

class AdminRequset extends Request {

  constructor() {
    super({
      baseURL: '/api',
      timeout: 5000,
    });
  }

  /**
   * token 过期
   * @param response 
   * @returns 
   */
  401(response: AxiosResponse<any, any>): Promise<any> {
    const data = response.data;
    ElMessageBox.close();
    ElMessageBox.confirm('登录信息已过期，请重新登录', '提示', {
      confirmButtonText: '确认',
      cancelButtonText: '取消',
      type: 'warning',
    }).then(() => {
      storeUser.signOut();
    }).catch(() => {});
    return Promise.reject(data);
  }

}

const request = new AdminRequset();

export default function(config: SateConfig) {
  return asyncto(request.instance(config));
}
