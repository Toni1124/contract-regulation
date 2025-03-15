import { AnyObj } from "@/utils/type";
import request from "./request";

/**
 * 获取交易列表
 */
export function api_getChainTradingList(params: AnyObj) {
  // return request({
  //   url: '/chain/queryChain',
  //   method: 'get',
  //   params,
  // })
  return Promise.resolve([null, {
    code: 200,
    data: {
      data: [
        {
          chainId: 'd592d7c1560d8b658227d12abbd26c02',
          name: '主链',
          byUserName: 'count_one',
          tag: '1005',
          status: 1,
        }
      ],
      totalCount: 10,
    },
  }])
}
