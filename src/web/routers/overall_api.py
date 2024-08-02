from pydantic import BaseModel
from src.utils.common import *
from src.api.easyquotation_executor import EasyQuotationExecutor
from src.utils.stock_utils import staistics_zdt_group
import akshare as ak
from src.crawls.stock_market_legu import *
from fastapi import APIRouter
from src.database.mongodb_utils import MongoDBUtil
from src.analysis.analysis import *

router = APIRouter()

class GetByDate(BaseModel):
    date:str = None

@router.post('/overall/zs')
async def get_zs_real_time_data():
    """获取三大指数实时数据"""
    res = {'code':200, 'data':[], 'msg':'请求成功'}
    try:
        data = EasyQuotationExecutor().get_zs_hq()
        res['data'] = data
    except Exception as e:
        print(e)
        res['code'] = 500
        res['msg'] = str(e)
    finally:
        return res

@router.post('/overall/zt')
async def get_zt_stocks(param:GetByDate=None):
    """获取涨停池并分组"""
    res = {'code':200, 'data':[], 'msg':'请求成功', 'groupData':{'name':"涨停分析", 'value':'', 'children':[]}, 'marketValueDistribute':{}}
    if param is None or param.date is None:
        date = get_current_today()
    else:
        date = param.date
        date = date.replace('-', '')
    try:
        df = ak.stock_zt_pool_em(date=date)
        df['首次封板时间'] = df['首次封板时间'].apply(fmt_hour_time)
        df['最后封板时间'] = df['最后封板时间'].apply(fmt_hour_time)
        df_dict = dftodict(df)
        df_dict = stock_common_info_by_name(df_dict, '名称')
        df_dict = type2str(df_dict)
        res['marketValueDistribute'] = statistical_market_value_distribute(df_dict, market_value_key='流通市值')
        res['data'] = df_dict
        df_group = df.groupby('所属行业')
        for name, df_data in df_group:
            infos =  dftodict(df_data)
            res_g = {'name':name, 'children':[], 'value':f'涨停数:{len(infos)}'} #第二级行业名称
            for info in infos: #第三级 股票信息
                name = info.pop('名称')
                value = '连板数:'+ str(info['连板数'])
                index = info.pop('序号')
                children = []
                for k, v in info.items():
                    children.append({'name':k, 'value':scientific_number_convert(v)})
                stock_g = {'name':name, 'value':value, 'children':children}
                res_g['children'].append(stock_g)
            res['groupData']['children'].append(res_g)
    except Exception as e:
        print(e)
        res['code'] = 500
        res['msg'] = str(e)
    finally:
        return res 

@router.post('/overall/hq')
async def get_hq_stocks():
    """获取赚钱效应分析"""
    res = {'code':200, 'data':[], 'msg':'请求成功'}
    try:
        df = stock_market_activity_legu().fillna(-1)
        df_dict = dftodict(df)
        df_dict[2] = {'item':df_dict[2]['item']+'(非一字无量涨停)',
                      'value':df_dict[2]['value']}
        df_dict[6] = {'item':df_dict[6]['item']+'(非一字无量跌停)',
                      'value':df_dict[6]['value']}
        sz_res_info = {
            'name':'上涨信息',
            'subItems':df_dict[:4],
            'date':df_dict[-1]
        }
        xd_res_info = {
            'name':'下跌信息',
            'subItems':df_dict[4:8],
            'date':df_dict[-1]
        }
        oter_res_info = {
            'name':'其他信息',
            'subItems':df_dict[8:-1],
            'date':df_dict[-1]
        }
        res['data'] = [sz_res_info, xd_res_info, oter_res_info]
    except Exception as e:
        print(e)
        res['code'] = 500
        res['msg'] = str(e)
    finally:
        return res 

@router.post('/overall/dt')
async def get_dt_stocks(param:GetByDate=None):
    """获取跌停池并分组"""
    res = {'code':200, 'data':[], 'msg':'请求成功', 'groupData':{'name':"跌停分析", 'value':'', 'children':[]}, 'marketValueDistribute':[]}
    if param is None or param.date is None:
        date = get_current_today()
    else:
        date = param.date
        date = date.replace('-', '')
    try:
        df = ak.stock_zt_pool_dtgc_em(date=date)
        if len(df)==0:
            res['msg'] = '无数据'
            return res
        df['最后封板时间'] = df['最后封板时间'].apply(fmt_hour_time)
        df_dict = dftodict(df)
        df_dict = stock_common_info_by_name(df_dict, '名称')
        df_dict = type2str(df_dict)
        res['marketValueDistribute'] = statistical_market_value_distribute(df_dict, market_value_key='流通市值')
        res['data'] = df_dict
        df_group = df.groupby('所属行业')
        for name, df_data in df_group:
            infos =  dftodict(df_data)
            res_g = {'name':name, 'children':[], 'value':f'跌停数:{len(infos)}'} #第二级行业名称
            for info in infos: #第三级 股票信息
                name = info.pop('名称')
                value = '连续跌停:'+ str(info['连续跌停'])
                index = info.pop('序号')
                children = []
                for k, v in info.items():
                    children.append({'name':k, 'value':scientific_number_convert(v)})
                stock_g = {'name':name, 'value':value, 'children':children}
                res_g['children'].append(stock_g)
            res['groupData']['children'].append(res_g)
    except Exception as e:
        res['code'] = 500
        res['msg'] = str(e)
    finally:
        return res 

@router.post('/overall/market')
async def get_market_infos():
    """全市场分析"""
    res = {'code':200, 'data':[], 'msg':'请求成功', 'dates':[], 'rawData':[]}
    try:
        dates = get_time_before_n(n=5)
        tmp_results = {}
        data_key = []
        for i, date in enumerate(dates):
            db_res = MongoDBUtil().get_real_time_data(id=date, auto_get=i==0) #当天的数据重新获取
            analysis_res = static_open_data(infos=db_res)
            if len(data_key)==0:
                data_key = list(analysis_res.keys())
            tmp_results[date] = analysis_res
        data = {}
        for key in data_key:
            for date in dates:
                count = len(tmp_results[date][key])
                count = count if count>0 else None
                if key not in data.keys():
                    data[key] = [count]
                else:
                    data[key].append(count)
        res['data'] = data
        res['dates'] = dates
        res['dataKey'] = data_key
        res['rawData'] = tmp_results 
    except Exception as e:
        print(e)
        res['code'] = 500
        res['msg'] = str(e)
    finally:
        return res 

@router.post('/overall/market_zdf_group')
async def get_market_infos_zdf():
    """全市场分析实时涨跌幅统计"""
    res = {'code':200, 'xData':[], 'msg':'请求成功', 'yData':[]}
    try:
        statistics_res, raw_df = staistics_zdt_group()
        res['xData'] = list(statistics_res.keys())
        res['yData'] = list(statistics_res.values())
    except Exception as e:
        print(e)
        res['code'] = 500
        res['msg'] = str(e)
    finally:
        return res 