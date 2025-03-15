import { AnyObj } from "@/utils/type";
import request from "./request";

const baseURL = '/permissions';

/**
 * 获取所有角色
 */
export function api_getRoleList(params: AnyObj) {
  return request({
    baseURL,
    url: '/v1/api/roles/list',
    params,
  })
}

/**
 * 新增角色
 */
export function api_addRole(data: AnyObj) {
  return request({
    baseURL,
    url: '/v1/api/roles/add',
    method: 'post',
    data,
  })
}

/**
 * 修改角色
 */
export function api_modifyRole(data: AnyObj) {
  return request({
    baseURL,
    url: '/v1/api/roles/modify',
    method: 'post',
    data,
  })
}

/**
 * 删除角色
 */
export function api_deleteRole(data: AnyObj) {
  return request({
    baseURL,
    url: '/v1/api/roles/delete',
    method: 'post',
    data,
  })
}

/**
 * 获取所有菜单
 */
export function api_getMenuList(params: AnyObj) {
  return request({
    baseURL,
    url: '/v1/api/menu/list',
    method: 'get',
    params,
  })
}

/**
 * 添加菜单
 */
export function api_addMenu(data: AnyObj) {
  return request({
    baseURL,
    url: '/v1/api/menu/add',
    method: 'post',
    data,
  })
}

/**
 * 修改菜单
 */
export function api_modifyMenu(data: AnyObj) {
  return request({
    baseURL,
    url: '/v1/api/menu/modify',
    method: 'post',
    data,
  })
}

/**
 * 删除菜单
 */
export function api_deleteMenu(data: AnyObj) {
  return request({
    baseURL,
    url: '/v1/api/menu/delete',
    method: 'post',
    data,
  })
}


// #region 接口
/**
 * 获取所有接口
 */
export function api_getInterfaceList(params: AnyObj) {
  return request({
    baseURL,
    url: '/v1/api/interface/list',
    method: 'get',
    params,
  })
}

/**
 * 添加接口
 */
export function api_addInferface(data: AnyObj) {
  return request({
    baseURL,
    url: '/v1/api/interface/add',
    method: 'post',
    data,
  })
}

/**
 * 修改接口
 */
export function api_modifyInferface(data: AnyObj) {
  return request({
    baseURL,
    url: '/v1/api/interface/modify',
    method: 'post',
    data,
  })
}

/**
 * 删除接口
 */
export function api_deleteInterface(data: AnyObj) {
  return request({
    baseURL,
    url: '/v1/api/interface/delete',
    method: 'post',
    data,
  })
}

// #endregion

/**
 * 获取所有元素
 */
export function api_getElementList(params: AnyObj) {
  return request({
    baseURL,
    url: '/v1/api/element/list',
    method: 'get',
    params,
  })
}

/**
 * 添加元素
 */
export function api_addElement(data: AnyObj) {
  return request({
    baseURL,
    url: '/v1/api/element/add',
    method: 'post',
    data,
  })
}

/**
 * 修改元素
 */
export function api_modifyElement(data: AnyObj) {
  return request({
    baseURL,
    url: '/v1/api/element/modify',
    method: 'post',
    data,
  })
}

/**
 * 删除元素
 */
export function api_deleteElement(data: AnyObj) {
  return request({
    baseURL,
    url: '/v1/api/element/delete',
    method: 'post',
    data,
  })
}

/**
 * 批量同步
 */
export function api_batchSynchronization(data: AnyObj) {
  return request({
    baseURL,
    url: '/v1/api/correlation/synchronization',
    method: 'post',
    data,
  })
}
/**
 * 调整同级顺序
 */
export function api_modifyOrder(data: AnyObj) {
  return request({
    baseURL,
    url: '/v1/api/menu/sort',
    method: 'post',
    data,
  })
}