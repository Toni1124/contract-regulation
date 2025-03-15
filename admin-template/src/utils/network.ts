import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse, InternalAxiosRequestConfig } from "axios";
import { ElMessage, ElNotification, ElLoading } from "element-plus";
import { getToken } from "./auth";

export interface SateConfig extends AxiosRequestConfig {
  noTips?: boolean
  noLoading?: boolean
  immediate?: boolean
}


let nowRquestCount = 0;
let loading = null;

export class Request {

  config: SateConfig
  instance: AxiosInstance

  /**
   * 拦截器封装，对返回数据进行了简单处理
   * @note 断网提示，统一报错
   * @note 适用于多个模块共用一个 token 的情况
   * @param config 
   */
  constructor(config: SateConfig) {

    fractureTips();
    this.config = config;
    this.instance = axios.create(config);

    this.instance.interceptors.request.use(this.requestUse)

    this.instance.interceptors.response.use((response) => {
      nowRquestCount --;
      return this.responseUse(response);
    }, error => {
      nowRquestCount --;
      const { response, config, message } = error;
      !config && ElMessage.error(message);  // 配置项中出现了特殊字符导致请求发送不了
      !(config as SateConfig).noLoading && nowRquestCount === 0 && loading.close();

      if (response && response.data) return this.responseUse(response);   

      // 响应出现错误（连接超时/网络断开/服务器忙没响应）
      ElNotification.closeAll();
      ElNotification({
        title: '网络可能存在一些问题',
        message: message || '错误原因：网络断开/无法连接/网络差/连接超时/服务器忙，请尝试重新操作或刷新页面',
        duration: null,
      })
      
      // 返回统一数据格式，不会导致代码取不到 code 而报错
      const { url } = error.config;
      return Promise.reject({
        code: 500,
        msg: message || 'network error: ' + url,
      });
    })
  }

  /**
   * 请求拦截
   * @note 多个子系统共用一个 token，不共用时请重写
   * @param config 
   * @returns 
   */
  requestUse(config: InternalAxiosRequestConfig) {
    !(config as SateConfig).noLoading && (loading = ElLoading.service());
    nowRquestCount ++;
    const auth = getToken();
    if (auth) {
      config.headers.Authorization = auth;
    }
    return config;
  }

  /**
   * 统一拦截处理
   * @param response 
   * @returns 
   */
  responseUse(response: AxiosResponse<any, any>): Promise<any> {
    const data = response.data;
    const config: SateConfig = response.config;
    if (config.immediate) {
      return Promise.resolve(data);
    }
    !(config as SateConfig).noLoading && nowRquestCount === 0 && loading.close();
    // 找对应的处理函数，没有的话交给 this.error 处理
    const handleFunc = this[data.code] || this.error;
    return handleFunc(response);
  }

  /**
   * 请求成功
   * @param response 
   * @returns 
   */
  200(response: AxiosResponse<any, any>): Promise<any> {
    return Promise.resolve(response.data);
  }

  /**
   * 请求失败
   * @param response 
   * @returns 
   */
  error(response: AxiosResponse<any, any>): Promise<any> {
    const { data, config } = response;
    !(config as SateConfig).noTips && ElMessage.error(data.message);
    return Promise.reject(data);
  }

}



/**
 * 请求函数封装，以数组形式返回
 * @param promise 请求函数
 * @param errorExt 
 * @returns [err, res] 通常情况下只有一项为 null
 */
export function asyncto(promise: Promise<any>) {
  return promise
    .then(data => [ null, data ])
    .catch(err => [ err, null ]);
}



/**
 * 断网提示
 */
export function fractureTips() {
  window.addEventListener('online', () => {
    ElMessage.closeAll();
    ElMessage.success('网络恢复');
  })
  window.addEventListener('offline', () => {
    ElMessage({
      type: 'error',
      message: '网络中断',
      duration: 0,
      showClose: true
    });
  })
}