import { AnyObj } from "./src/utils/type";

declare const process: AnyObj;

export const DEVELOPMENT = 'development';
export const PRODUCTION  = 'production';

// 生产环境
let env = {

  NODE_ENV: process.env.NODE_ENV as typeof DEVELOPMENT | typeof PRODUCTION,

  BASE_ROUTE_URL: process.env.VUE_APP_PUBLICPATH,

  BASE_URL: '/admin-template'

};

export default Object.freeze(env);
