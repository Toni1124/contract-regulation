
/**
 * 分页索引计算
 * @param pageNumber 
 * @param pageSize 
 * @param index 
 * @returns 
 */
export function pagingIndex(pageNumber: number, pageSize: number, index: number) {
  return (pageNumber - 1) * pageSize + index + 1;
}

/**
 * 数字生成器
 * @call const iter = createNum(); iter.next().value;
 */
export function* createNum() {
  let n = 0
  while (true) {
    yield n;
    n++;
  }
}
