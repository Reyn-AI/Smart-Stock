from typing import List, Dict
from src.utils.common import *
import math
from copy import deepcopy
from src.utils.registy import analysis_register_history
from src.utils.stock_utils import *
import talib
from src.utils.constant import BAO_STOCK_NAME
from concurrent.futures import ThreadPoolExecutor
from .base import BaseAnalysis

        
@analysis_register_history(name='窗口时间内走势角度选股策略', params=[{'code':'timeperiod', 'name':"窗口长度(天)", 'default':15, 'uiType':'input'},
                                            {'code':'angle', 'name':"角度阈值", 'default':10, 'uiType':'input'},
                                            {'name':'k线类型', 'code':'frequency', 'default':'d', 'uiType':'selectDate'},
                                            {'code':'startDate', 'name':'开始日期', 'uiType':'date', 'default':''},
                                             {'code':'endDate', 'name':'结束日期', 'uiType':'date', 'default':''}])
class TaLibDataAnalysisSelectByAngle(BaseAnalysis):
    """根据角度策略选股"""
    
    
    async def analysis(self, *args, **kwargs):
        """根据角度策略选股"""
        all_codes = get_all_stock_codes(market=self.market)
        # try:
        start_date = [self.startDate] * len(all_codes)
        end_date = [self.endDate] * len(all_codes)
        frequencys = [self.frequency] * len(all_codes)
        with ThreadPoolExecutor(max_workers=1 if self.frequency !='d' else 30) as executor:
            results = executor.map(self.single_analysis, all_codes, start_date, end_date, frequencys)
        results = [x for y in results for x in y]
        return results
        # except Exception as e:
        #     self.logger.error("TuShareDataAnalysisSelectByAngle:"+str(e))
        #     breakpoint()
        

    def single_analysis(self, code, start_date, end_date, frequency):
        res_codes = []
        df = get_day_k_data(code=code,
                                    start_date=start_date,
                                    end_date=end_date,
                                    frequency=frequency,
                                    api_type='abu' if frequency=='d' else 'baostock')
        if df is None or len(df)==0:
            return res_codes
        angles = talib.LINEARREG_ANGLE(df.close, timeperiod=int(self.timeperiod)).to_list()
        if angles[-1]>float(self.angle):
            data = df.iloc[-1].to_dict()
            TUSHARE_TYPE_NAME.update(BAO_STOCK_NAME)
            data = type2str(data, type_str_dict=TUSHARE_TYPE_NAME)
            name = LoadJsonInfo().get_name_by_code(code)
            if name is not None:
                data['股票名字'] = name
            data[f'{self.timeperiod}收盘线角度'] = angles[-1]
            res_codes.append(data)
            # self.logger.info(f'TaLibDataAnalysisSelectByAngle: {code}, {angles[-1]}')
        return res_codes

if __name__ == '__main__':
    params = {'name':'窗口时间内走势角度选股策略', 'params':[{'code':'timeperiod', 'name':"窗口长度", 'default':10, 'uiType':'input'},
                                            {'code':'angle', 'name':"角度阈值", 'default':1, 'uiType':'input'},
                                            {'name':'k线类型', 'code':'frequency', 'default':'d', 'uiType':'select'},
                                            {'code':'startDate', 'name':'开始日期', 'uiType':'date', 'default':'2024-01-01'},
                                             {'code':'endDate', 'name':'结束日期', 'uiType':'date', 'default':'2025-01-01'}]}
    codes = TaLibDataAnalysisSelectByAngle(params=params).analysis()
    print(codes)