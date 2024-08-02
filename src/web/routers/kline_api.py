from fastapi import APIRouter
from pydantic import BaseModel
from src.utils.common import *
from src.utils.stock_utils import *
import akshare as ak
from src.api.baostock_executor import BaoStockExecutor
router = APIRouter()

class SelectDayItem(BaseModel):
    """获取单个股票近n年日k线数据
       {
           strategyParams:[{'code':'策略类名', 'params':[{'code':'参数1名','value':参数1值}]}],
           marketParams:[0,1,2,3]
       }
    """
    code: str = 'sh000001' #股票代码
    nYear: float = 2 #近多少年数据
    support: bool = False #可视化支撑压力线
    startDate:str = None
    endDate:str = None
    

    
@router.post('/kline/day')
async def find_day_k_line_data(param:SelectDayItem):
    """获取日线数据"""
    res = {'code':200, 'rawData':[], 'msg':'请求成功', 'supportData':{}}
    try:
        code = param.code
        n_fold = param.nYear
        df = get_day_k_data(code=code, n_folds=n_fold, start_date=param.startDate, end_date=param.endDate, return_list=True, api_type='abu')
        df_res = dftodict(df)
        res['rawData'] = df_res
    except Exception as e:
        print(e)
        res['code'] = 500
        res['msg'] = str(e)
    finally:
        return res



class RealTimeItem(BaseModel):
    """实时分时数据
       {
           strategyParams:[{'code':'策略类名', 'params':[{'code':'参数1名','value':参数1值}]}],
           marketParams:[0,1,2,3]
       }
    """
    code: str = 'sh000001' #股票代码

@router.post('/kline/fenshi')
async def fenshi_k(params:RealTimeItem):
    res ={'code':200, 'msg':'请求成功', 'data':[], 'date':[], 'meanData':[]}
    try:
        code = params.code
        hourData = []
        code = code_to_abu_code(code)
        df = ak.stock_zh_a_tick_tx_js(symbol=code)
        date = df['成交时间'].to_list()
        df['均线'] = round(df['成交金额'].cumsum()/df['成交量'].cumsum()/100,2)
        for i, item in df.iterrows():
            item = item.to_list()
            hourData.append(item)
        res['hourData'] = hourData
        data = dftodict(df)
        res['data'] = data
        res['date'] = date
        res['meanData'] = df['均线'].to_list()
        
    except Exception as e:
        res['code'] = 500
        res['msg'] = str(e)
    finally:
        return res

class KLineItem(SelectDayItem):
    frequency:str = 'd'

@router.post('/kline/kline_by_freq')
def get_k_line_by_frequency(param:KLineItem):
    """通过频率获取k线数据"""
    res = {'code':200, 'rawData':[], 'msg':'请求成功'}
    try:
        code = param.code
        df = BaoStockExecutor().get_history_time_data(code=code, start_date=param.startDate, end_date=param.endDate, frequency=param.frequency)
        res['rawData'] = df
    except Exception as e:
        print(e)
        res['code'] = 500
        res['msg'] = str(e)
    finally:
        return res
    
    

    