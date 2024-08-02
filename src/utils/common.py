import importlib.util
from typing import Dict, List, Union
import logging
from pathlib import Path
import time
import os, sys
import json
import datetime as dt
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from copy import deepcopy
from src.utils.tushare_constant import *
import uuid
import math
import holidays
import qstock as qs
from functools import lru_cache
import importlib

def is_chinese_hoildays(date:datetime.date):
    holidays_ = holidays.China()
    return date in holidays_

logger = None

def list_convert_science_number(infos: List, keys:List):
    """将列表里指定的key的大数进行转换"""
    if not isinstance(keys, List):
        keys = [keys]
    for info in infos:
        for key in keys:
            if key in info.keys():
                info[key] = scientific_number_convert(info[key])
    return infos
def get_uuid():
    uid = uuid.uuid4()
    return str(uid)

def get_current_today():
    # 获取当前日期
    current_date = dt.date.today()
    return str(current_date).replace('-', '')

def get_project_dir():
    """获取工程根目录"""
    return str(Path(__file__).resolve().parents[2])


def get_default_output_path():
    """获取默认输出路径"""
    default_dir =  os.path.join(get_project_dir(), ".smart_stock_outputs", get_time())
    os.makedirs(default_dir, exist_ok=True)
    return default_dir

def get_time(template="%Y_%m_%d_%H_%M"):
    """获取格式化时间"""
    return time.strftime(template, time.localtime())

def get_time_before_n(n=5, template='%Y-%m-%d', skip_holiday=True):
    """获取当前日期的前n天日期"""
    now = datetime.now()
    dates = []
    time_delta = 0
    while True:
        if skip_holiday:
            time_delta = 1
            weekday = now.weekday()
            if weekday in [5, 6] or is_chinese_hoildays(now.date()):
                now = now - timedelta(days=time_delta)
                continue
            else:
                dates.append(now.strftime(template))
                now = now - timedelta(days=time_delta)
        else:
            dates.append((now - timedelta(days=time_delta)).strftime(template))
            time_delta += 1
        if len(dates) == n:
            break
    return dates

def get_logger(log_path=os.path.join(get_default_output_path(), 'smart-stock.log')):
    """获取logger"""
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    global logger
    if logger is None:
        logger = logging.getLogger(__name__)
        logger.setLevel(level=logging.INFO)
        stream_handler = logging.StreamHandler(sys.stderr)
        handler = logging.FileHandler(log_path, mode="w")
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.addHandler(stream_handler)
    else:
        return logger
    return logger


def save_json(infos, path):
    """dump json"""
    with open(path, "w", encoding='utf-8') as f:
        json.dump(infos, f, ensure_ascii=False, indent=8)
    get_logger().info("Json Dump in %s", path)

def load_json(path):
    """load json数据"""
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    # get_logger().info("Load json data from %s", path)
    return data

def scientific_number_convert(number:Union[str, float]):
    """科学数字转换"""
    try:
        if isinstance(number, (float, int)) or (isinstance(number, str) and number.isnumeric()):
            if abs(float(number)) >= 1e7:
                number = float(number)
                number = round(number/1e8, 4)
                number =  f"{number} 亿"
            # elif abs(number)>=1e4:
            #     number = round(number/1e4, 4)
            #     return f"{number} 万"
    except Exception as e:
        pass
    finally:
        return str(number)

def reverse_dict(data:Dict):
    """反转字典"""
    data = {v:k for k,v in data.items()}
    return data

def get_stock_list_by_key(key, value, db_path = None):
    """根据key获取同类股票, 如包含某个概念或某个行业板块所有股票代码和名称
        key: 
            z50: 行业
            z52: 地域
            z53: 概念
        db_path:
            存放基础信息的json路径
    """
    datasets = os.path.join(str(Path(__file__).resolve().parents[2].joinpath('data/common_infos_all_stocks.json'))) \
                if db_path is None else db_path
    datasets = load_json(datasets)
    res = []
    for item in datasets:
        if key in item.keys():
            if value in item[key]:
                res.append(item['code'])
    return res



def format_ts_code(codes:List):
    """format 股票代码"""
    ts_codes = []
    for x in codes :
        x = str(x).upper()
        if x.startswith('39') and not x.endswith('SZ'):
            code = x + '.SZ'
        elif x.startswith('30') and not  x.endswith('SZ'):
            code = x + '.SZ'
        elif x.startswith('0') and not x.endswith('SZ'):
            code = x + '.SZ'
        elif x.startswith('6') and not x.endswith('SH'):
            code = x + '.SH'
        elif x.startswith('8') and not x.endswith('BJ'):
            code = x + '.BJ'
        elif x.startswith('4') and not x.endswith('BJ'):
            code = x + '.BJ'
        else:
            code = x
        if len(code.split('.'))>1:
            ts_codes.append(code)
    return ts_codes

def time_str_to_datetime(time_str):
    """转换字符串时间到datetime格式"""
    time_str = datetime.strptime(time_str, "%Y-%m-%d")
    return time_str

def cal_increase(pre_close:float, now_price:float):
    """计算涨幅"""
    if pre_close==0 or now_price==0:
        return 0
    diff = now_price - pre_close
    incr = round(diff/pre_close, 4)
    return round(incr*100, 2)

def fmt_time(date_str, template='%Y-%m-%d %H:%M:%S', custom_format = "%Y%m%d%H%M%S%f"):
    """将形如20240509133000000 时间戳转为标准日期格式"""
    #from datetime import datetime
    # 使用strptime将自定义格式的日期字符串转换为datetime对象
    datetime_obj = datetime.strptime(date_str, custom_format)
    
    # 使用strftime将datetime对象转换为标准格式
    formatted_date = datetime_obj.strftime(template)
    return formatted_date


def get_all_stock_codes(path=None, market: list=None):
    from src.utils.stock_utils import get_codes_by_zs_code, get_all_market_codes
    res = get_all_market_codes()
    if res is None:
        json_path = str(Path(__file__).resolve().parents[2].joinpath('data/common_infos_all_stocks_mapping.json')) if path is None else path
        data = load_json(json_path)
        res = [x['code'] for x in data.values()]
    if market is not None:
        codes = []
        for code in market:
            if str(code) == '1':
                codes.append('0') #深证
            if str(code) == '2':
                codes.append('60') #上证
            if str(code) == '3':
                codes.extend(['8', '4']) #北证
            if str(code) == '4': #创业板
                codes.extend(['30'])
            if str(code) == '5': #科创
                codes.append('68')
            if str(code) == '6':
                codes.extend(get_codes_by_zs_code('kc50'))
            if str(code) == '7':
                codes.extend(get_codes_by_zs_code('hs300'))
            if str(code) == '8':
                codes.extend(get_codes_by_zs_code('sz50'))
            if str(code) == '9':
                codes.extend(get_codes_by_zs_code('zz1000'))
        res = list(filter(lambda x: x.startswith(tuple(codes)), res))
    return res

def group_codes(codes:List, number=50)->List[List]:
    """切分成小份"""
    tmp_codes = []
    group_codes = []
    if len(codes)<number:
        return [codes]
    for code in codes:
        tmp_codes.append(code)
        if len(tmp_codes)==number:
            group_codes.append(tmp_codes)
            tmp_codes = []
    if len(tmp_codes)>0:
        group_codes.append(tmp_codes)
    return group_codes


def statistical_market_value_distribute(infos: List, market_value_key):
    """统计市值分布"""
    res = {'0-50亿':0, '50-100亿':0,'100-200亿':0, '200-300亿':0, '300-500亿':0, '>500亿':0}
    for info in infos:
        value = info[market_value_key]
        if float(value)<=5e9:
            res['0-50亿'] += 1
        elif float(value)>5e9 and float(value)<=1e10:
            res['50-100亿'] += 1
        elif float(value)>1e10 and float(value)<=2e10:
            res['100-200亿'] += 1
        elif float(value)>2e10 and float(value)<=3e10:
            res['200-300亿'] += 1
        elif float(value)>3e10 and float(value)<=5e10:
            res['300-500亿'] += 1
        elif float(value)>5e10 :
            res['>500亿'] += 1
    res = [{'name':k, 'value':v} for k,v in res.items()]
    return res
    
def type2str(data: Union[List[Dict], Dict]):
    """stype to name"""
    data = deepcopy(data)
    if isinstance(data, List):
        for item in data:
            keys = list(item.keys())
            for k in keys:
                item[TUSHARE_TYPE_NAME.get(k, k)] = item.pop(k)
    elif isinstance(data, Dict):
        for k, v in data.items():
            for item in v:
                keys = list(item.keys())
                for k in keys:
                    item[TUSHARE_TYPE_NAME.get(k, k)] = item.pop(k)
    return data

def stock_common_info_by_name(infos:List, name_key):
    """传入列表封装股票基本信息"""
    common_info = LoadJsonInfo()
    for info in infos:
        name = info[name_key]
        inf_dict = common_info.load_concept_from_wzw_data(name)
        info.update(inf_dict)
    return infos

def singleeton_func(cls):
    instance={}
    def _singleton(*args, **kwargs):
        if cls not in instance:
            instance[cls] = cls(*args, **kwargs)
        return instance[cls]
    return _singleton

@singleeton_func
class LoadJsonInfo():
    def __init__(self, path=None):
        json_path = str(Path(__file__).resolve().parents[2].joinpath('data/common_infos_all_stocks_mapping.json')) if path is None else path
        self.data = load_json(json_path)
        self.data_code_mapping = {x['code']:x for x in self.data.values()}
    def load_concept_from_wzw_data(self, name):
        """通过name查询概念"""
        if name in self.data.keys():
            return self.data.get(name)
        return {}
    def get_code_by_name(self, name):
        if name in self.data.keys():
            return self.data[name]['code']
        return None
    def get_name_by_code(self, code):
        code = code.split('.')[-1]
        if code in self.data_code_mapping.keys():
            return self.data_code_mapping[code]['name']
        return None
    def stock_name_exist(self, name):
        return name in self.data.keys()
def fmt_hour_time(date):
    """format 6位时间"""
    if len(date)>6:
        return date
    date = "%s:%s:%s" % (date[0:2], date[2:4], date[4:])
    return date
def fmt_date(convert_date):
    """
    将时间格式如20160101转换为2016-01-01日期格式, 注意没有对如 201611
    这样的做fix适配，外部需要明确知道参数的格式，针对特定格式，不使用时间api，
    直接进行字符串解析，执行效率高
    :param convert_date: 时间格式如20160101所示，int类型或者str类型对象
    :return: %Y-%m-%d日期格式str类型对象
    """
    convert_date = str(convert_date)
    if '-' in str(convert_date):
        return convert_date
    if isinstance(convert_date, float):
        # float先转换int
        convert_date = int(convert_date)
    convert_date = str(convert_date)

    if len(convert_date) > 8 and convert_date.startswith('20'):
        # eg '20160310000000000'
        convert_date = convert_date[:8]

    if '-' not in convert_date:
        if len(convert_date) == 8:
            # 20160101 to 2016-01-01
            convert_date = "%s-%s-%s" % (convert_date[0:4],
                                         convert_date[4:6], convert_date[6:8])
        elif len(convert_date) == 6:
            # 201611 to 2016-01-01
            convert_date = "%s-0%s-0%s" % (convert_date[0:4],
                                           convert_date[4:5], convert_date[5:6])
        else:
            raise ValueError('fmt_date: convert_date fmt error {}'.format(convert_date))
    return convert_date

def code_to_abu_code(code:str):
    """加入sz/sh前缀"""
    if code.startswith(('sh', 'sz', 'bj')):
        return code
    new_code = []
    for c in code:
        if c.isnumeric():
            new_code.append(c)
    x = ''.join(new_code)
    if x.startswith('39'):
        code = 'sz' + x
    elif x.startswith('30'):
        code = 'sz' + x
    elif x.startswith('0'):
        code = 'sz' + x
    elif x.startswith('6'):
        code = 'sh' + x
    elif x.startswith('8'):
        code = 'bj' + x
    elif x.startswith('4'):
        code = 'bj' + x
    else:
        code = x
    return code

def code_to_bao_code(code:str):
    """加入sz/sh前缀"""
    if code.startswith(('sh.', 'sz.', 'bj.')):
        return code
    if code.startswith(('sh', 'sz', 'bj')):
        code = code.replace('sh', 'sh.').replace('sz', 'sz.').replace('bj', 'bj.')
        return code
    new_code = []
    for c in code:
        if c.isnumeric():
            new_code.append(c)
    x = ''.join(new_code)
    if x.startswith('39'):
        code = 'sz.' + x
    elif x.startswith('30'):
        code = 'sz.' + x
    elif x.startswith('0'):
        code = 'sz.' + x
    elif x.startswith('6'):
        code = 'sh.' + x
    elif x.startswith('8'):
        code = 'bj.' + x
    elif x.startswith('4'):
        code = 'bj.' + x
    else:
        code = x
    return code

def cal_amplitude(high, low, pre_close):
    """计算振幅"""
    if pre_close==0:
        return 0
    return round(100* (high - low)/pre_close, 2)
    
def cal_hslv(ltgb, cjl):
    """计算换手率"""
    if ltgb == 0:
        return 0
    return round(100*cjl/ltgb,2)


def abu_code_to_code(code:str):
    """只保留数字"""
    new_code = []
    for c in code:
        if c.isnumeric():
            new_code.append(c)
    x = ''.join(new_code)
    return x

def tushare_dict_to_df(items:List[Dict]):
    """字典转datafram"""
    if len(items) == 0:
        return None
    keys = items[0].keys()
    dict_item = {}
    for key in keys:
        dict_item.update({key:[ x[key] for x in items]})  
    df = pd.DataFrame(dict_item)
    if 'date' in df:
        df.date = pd.to_datetime(df.date.apply(fmt_date))
    if 'trade_date' in df:
        df.trade_date = pd.to_datetime(df.trade_date.apply(fmt_date))
    return df
    
def dftodict(df:pd.DataFrame)->Dict:
    "df转list[dict]"
    if not isinstance(df, pd.DataFrame):
        return df
    if df is None:
        return None
    keys = [x.lower() for x in list(df.columns)]
    res = []
    for values in df.values:
        data  = dict(zip(keys, list(values)))
        res.append(data)
    
    return res

def numpy2list(data: Dict):
    """numpy数组转list"""
    res_data = {}
    for k,v in data.items():
        res_data[k] = [x.tolist() for x in v]
    return res_data
    
def cal_vwap(df: pd.DataFrame):
    """vwap计算"""
    mean_price = (df['high'].astype(float) + df['low'].astype(float))/2
    vwap = (df['volume'].astype(float)*mean_price).sum()/df['volume'].astype('float').sum()
    return round(vwap,2)

def cal_k_mean(df: pd.DataFrame):
    """计算分时均线"""
    if '成交金额' in df:
        df['mean'] = round(df['成交金额'].astype(float)/(df['成交量'].astype(float)*100), 2)
    else:
        df['mean'] = round((df['high'].astype(float) + df['low'].astype(float))/2, 2)
    return df

def list_nan_to_none(data):
    """将列表中的nan转为none"""
    res = []
    if isinstance(data, tuple):
        #处理元组
        for d in data:
            res_i = []
            if not isinstance(d, list) and hasattr(d, 'tolist'):
                d = d.tolist()
            for i in d:
                if math.isnan(i):
                    i = None
                res_i.append(i)
            res.append(res_i)
    else:
        for d in data:
            try:
                if not isinstance(d,str) and math.isnan(d):
                    d = None
            except Exception as e:
                pass
            res.append(d)
    return res

def type2str(datas: Union[List[Dict], Dict], type_str_dict: Dict=TUSHARE_TYPE_NAME):
    """stype to name"""
    data = deepcopy(datas)
    if isinstance(data, List):
        for item in data:
            keys = list(item.keys())
            for k in keys:
                item[type_str_dict.get(k.lower(), k)] = item.pop(k)
    elif isinstance(data, Dict):
        for k, v in datas.items():
            data[type_str_dict.get(k.lower(), k)] = data.pop(k)
    return data

def import_modules_from_py(modules_dir):
    """从文件导入module"""
    files = list(filter(lambda x : x.endswith('.py'), os.listdir(modules_dir)))
    modules = []
    for file in files:
        file_path = os.path.join(modules_dir, file)
        module_name = file.split('.')[0]
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        sys.modules[module_name] = module
        modules.append(module)
    return modules
    