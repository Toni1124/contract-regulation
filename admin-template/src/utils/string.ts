
/**
 * 劫持粘贴板
 * @param value 需要复制的字符
 */
export function copyToBoard(value: string | number) {
  const element: any = document.createElement('textarea');
  document.body.appendChild(element);
  element.value = value;
  element.select();
  if (document.execCommand('copy')) {
    document.execCommand('copy');
    document.body.removeChild(element);
    return true;
  }
  document.body.removeChild(element)
  return false;
}

/**
 * 首字母大写
 * @param text 
 * @returns 
 */
export function initialUppercase(text: string) {
  if (!text) return '';
  return text[0].toLocaleUpperCase() + text.slice(1);
}

/**
 * 字符串转大驼峰
 * @param text 
 * @returns 
 */
export function toGreatHump(text: string) {
  return text.split(/\-|\_/).map(val => initialUppercase(val)).join('');
}
