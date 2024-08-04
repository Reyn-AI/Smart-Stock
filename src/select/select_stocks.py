from src.utils.registy import analysis_register_history
from src.analysis.base import BaseAnalysis
from src.utils.stock_utils import *
from src.utils.common import *
from src.utils.tushare_constant import TUSHARE_TYPE_NAME
from src.utils.parallel_util import Parallel, delayed
import asyncio

@analysis_register_history(name='近期存在涨停的股票', params=[{'code':'N', 'name':"窗口长度(天)", 'default':7, 'uiType':'input'},
                                            {'code':'startDate', 'name':'开始日期', 'uiType':'date', 'default':'2024-02-07'},
                                             {'code':'endDate', 'name':'结束日期', 'uiType':'date', 'default':get_time("%Y-%m-%d")}])
class ExistZTDataAnalysisSelect(BaseAnalysis):
    """根据承压线选股"""
    
    async def analysis(self, *args, **kwargs):
        all_codes = get_all_stock_codes(market=self.market)
        try:
            codes = group_codes(all_codes)
            results_list = await asyncio.gather(*[self.analysis_multi(codes=x, start_date=self.startDate, end_date=self.endDate) for x in codes])
            results = [x for y in results_list for x in y]
            return results
        except Exception as e:
            self.logger.error("RSRSDataAnalysisSelect:"+str(e))
    
    async def analysis_multi(self, codes:list, start_date, end_date):
        res_codes = []
        df_list = get_day_k_data_multi(codes=codes,
                                    start_date=start_date,
                                    end_date=end_date,
                                    return_list=True,
                                    api_type='qstock')
        if df_list is None or len(df_list)==0:
            return res_codes
        results = Parallel(n_jobs=20, backend='process')([delayed(cal_exist_zt_in_windows)(df, windows=int(self.N)) for df in df_list])
        for r_df in results:
            if r_df.exist_zt[-1]:
                data = r_df.iloc[-1].to_dict()
                data = {k:str(v) for k,v in data.items()}
                data = type2str(data, type_str_dict=TUSHARE_TYPE_NAME)
                res_codes.append(data)
        return res_codes