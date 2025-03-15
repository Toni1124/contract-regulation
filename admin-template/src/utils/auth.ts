
const TOKEN = 'token';

/**
 * 获取 token
 * @returns 
 */
export function getToken() {
  return localStorage.getItem(TOKEN);
}

/**
 * 储存 token
 * @param value 
 */
export function setToken(value: string) {
  localStorage.setItem(TOKEN, value);
}

/**
 * 删除 token
 */
export function delToken() {
  localStorage.removeItem(TOKEN);
}
