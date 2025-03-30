import axios from 'axios'

const request = axios.create({
  baseURL: 'http://127.0.0.1:5000',  // 确保这里指向你的 Flask 后端地址
  timeout: 5000
})

// 响应拦截器
request.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

export default request
