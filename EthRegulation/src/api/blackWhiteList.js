import axios from 'axios'

// 创建axios实例
const api = axios.create({
  baseURL: 'http://localhost:5000/api',
  timeout: 5000
})

export const getBlackWhiteList = (params) => {
  return api.get('/black-white-list', { params })
}

export const addBlackWhiteList = (data) => {
  return api.post('/black-white-list', data)
} 