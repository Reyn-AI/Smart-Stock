"""执行器基类"""

from src.utils.common import get_logger, save_json, get_time,  get_default_output_path
from typing import Dict, List, Union
from abc import ABCMeta, abstractmethod
import sys
import os
from pathlib import Path
import requests
sys.path.append(str(Path(__file__).resolve().parents[1]))
import dataclasses
from src.items.base_item import StockBaseItem
from src.analysis.base import BaseAnalysis
from src.database.mysql_utils import MySQLUtils
from src.utils.db_constan import *
from src.utils.common import *
from src.utils.env import SAVE_JSON
import asyncio
from functools import partial


class BaseExecutor(metaclass=ABCMeta):
    """执行器基类"""

    def __init__(self, api_name: str, save_dir: str=None, *args, **kwargs):
        self.api_name = api_name
        self.save_dir = save_dir if save_dir is not None else  get_default_output_path()
        os.makedirs(self.save_dir, exist_ok=True)
        self.logger = get_logger(log_path=os.path.join(
            self.save_dir, "smart-stock-log.log"))
        self.request_count = 0
        self.mysql_utils = MySQLUtils(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
        self.all_codes = get_all_stock_codes()
        
    def _execute(self, url: str, params: Dict, data_key='data', request_type='post', *args, **kwargs) -> List[Dict]:
        """执行数据获取"""
        if request_type == 'post':
            self.logger.info("Post: %s, params: %s", url, params)
            response = requests.post(url=url, data=params, timeout=100)
        else:
            url = f"{url}?"
            params_str = []
            for k,v in params.items():
                params_str.append(f'{k}={v}')
            params = '&'.join(params_str)
            url += params
            self.logger.info("Get: %s", url)
            response = requests.get(url=url)
        if response.status_code != 200:
            self.logger.error("请求失败,错误代码: %s", response.status_code)
        if response.json()["code"] != 200:
            self.logger.error("请求失败:%s", response.json().get('message'))
            raise RuntimeError
        data = response.json()[data_key]
        self.request_count += 1
        if SAVE_JSON:
            save_json(data, os.path.join(
                self.save_dir, f"{get_time(template='%Y_%m_%d')}_{params.get('type',self.request_count)}_{self.request_count}_{os.path.basename(url)}.json"))
        return data

    def group_codes(self, codes:List, number=1)->List[List]:
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
     
    
    def get_data_from_api(self, api_type, *args, **kwargs) -> Dict:
        """根据传入类型调用不同接口获取数据"""
        func = getattr(self, f'get_{api_type}')
        if func is None:
            raise NotImplementedError
        res = func(*args, **kwargs)
        return res
    
    def _item2dict(self, data: List[StockBaseItem]):
        return [dataclasses.asdict(x) for x in data]

    def _data_wrapper(self, data: List[Dict], item_class: StockBaseItem):
        """json映射到实体类"""
        data_list = []
        for item in data:
            data_item = item_class(**item)
            data_list.append(data_item)

        return data_list
    
    def filter_codes_zb(self, codes):
        """只保留主板代码"""
        codes_res = []
        for code in codes:
            code = abu_code_to_code(code)
            if code.startswith(('60', '0')):
                codes_res.append(code)
        return codes_res
    
    def filter_data(self, info: List[Dict], codes=None):
        """过滤脏数据"""
        if len(info) == 0:
            return info
        if 'zsz' in info[0].keys():
            info = list(filter(lambda x: x['zsz'] > 0, info))
        if 'volume' in info[0].keys():
            info = list(filter(lambda x: x['volume'] > 0, info))
        if 'open' in info[0].keys():
            info = list(filter(lambda x: x['open'] > 0, info))
        if codes is not None:
            info = list(filter(lambda x: x['code'] in codes), info)
        return info
    
    def analysis(self, analyzer:List[BaseAnalysis], infos:Union[List[Dict], pd.DataFrame], **kwargs):
        """分析"""
        if analyzer is None:
            return {}
        if not isinstance(analyzer, list):
            analyzer = [analyzer]
        all_res = {}
        async_analyzer_func = [partial(analyzer_cls.analysis, infos=infos) for analyzer_cls in analyzer]
        try:
            for cls in analyzer:
                res = cls.analysis(infos=infos)
                all_res.update(res)
            # import nest_asyncio             
            # nest_asyncio.apply()
            # loop = asyncio.get_event_loop()
            # res = loop.run_until_complete(asyncio.wait([x() for x in async_analyzer_func]))
            # for r in list(res[0]):
            #     all_res.update(r.result())
            return all_res
        except Exception as e:
            self.logger.error(str(e))
            # raise RuntimeError(e)
            return {}
    
    def wrapper_res_use_wzw(self, infos:List[Dict]):
        """用wzw数据重新装饰并计算涨幅"""
        info_set = LoadJsonInfo()
        try:
            for info in infos:
                name = info.get('name')
                wrapper_dict = info_set.load_concept_from_wzw_data(name)
                info.update(wrapper_dict)
                if 'pre_close' in info.keys() and 'price' in info.keys():
                    increase = cal_increase(pre_close=info.get('pre_close',0), now_price=info.get('price', 0))
                    info.update({'zdfd': increase})
                # high = info['high']
                # low = info['low']
                # pre_close = info['pre_close']
                # zhfu = cal_amplitude(high=high, low=low, pre_close=pre_close)
                # info['zhfu'] = zhfu
                # info['hslv'] = cal_hslv(cjl=info['volume'], ltgb=info.get('ltgb', -1))
        except Exception as e:
            self.logger.error(f"{str(e)}, {str(info.get('ts_code'))}")
        return infos
    
    def type2str(self, data: Union[List[Dict], Dict], type_str_dict: Dict=TUSHARE_TYPE_NAME):
        """stype to name"""
        data = deepcopy(data)
        if isinstance(data, List):
            for item in data:
                keys = list(item.keys())
                for k in keys:
                    item[type_str_dict.get(k.lower(), k)] = item.pop(k)
        elif isinstance(data, Dict):
            for k, v in data.items():
                for item in v:
                    keys = list(item.keys())
                    for k in keys:
                        item[type_str_dict.get(k.lower(), k)] = item.pop(k)
        return data
