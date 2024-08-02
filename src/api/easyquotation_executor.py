from typing import List, Dict
from src.api.base import BaseExecutor
from src.utils.common import *
from src.utils.parallel_util import *
import pandas as pd
import easyquotation

@singleeton_func
class EasyQuotationExecutor(BaseExecutor):
    
    def __init__(self, api_name: str='easyquotation', save_dir: str = None, *args, **kwargs):
        super().__init__(api_name, save_dir, *args, **kwargs)
        api_type = kwargs.get("api_type", 'tencent') #sina tencent
        self.quotation = easyquotation.use(api_type)
        
    def get_market_snapshot(self, *args, **kwargs):
        """获取整个市场行情"""
        res = self.quotation.market_snapshot(prefix=False)
        return self.convert_format(res)
    
    def get_realtime_data_by_code(self, code, *args, **kwargs):
        """获取单个股票实时数据"""
        res = self.quotation.real(code)
        return res
    
    def convert_format(self, res, rename=False):
        """转换到List[Dict]格式"""
        results = []
        for k,v in res.items():
            v['code'] = k
            if rename:
                v['price'] = v.get('now', -1)
                v['amount'] = scientific_number_convert(v.get('成交额(万)', -1))
                v['volume'] = scientific_number_convert(v.get('成交量(手)', -1))
                v['change'] = v.get('涨跌(%)', -1)
            results.append(v)   
        return results
    
    def  get_zs_hq(self, codes:List=['sh000001','399001','399006'], *args, **kwargs):
        res = self.quotation.stocks(codes, prefix=True) 
        return self.convert_format(res, rename=True)


if __name__ == '__main__':
    res = EasyQuotationExecutor().get_zs_hq()
    breakpoint()