"""歪枣网数据获取执行器"""

from src.analysis.data_analysis import *
from src.utils.constant import USER_TOKEN
from src.utils.common import *
from src.view.excel import WZWExcel, BaseViewer
from src.items.base_item import *
from src.utils.constant import *
from src.api.base import BaseExecutor
from typing import Dict, List, Union
import sys
from pathlib import Path
import os
from src.utils.env import *
sys.path.append(str(Path(__file__).resolve().parents[2]))


class WZWExecutor(BaseExecutor):
    "歪枣网数据获取执行器"

    def __init__(self, api_name: str = "WZWAPI", save_dir=None, *args, **kwargs):
        save_dir = get_default_output_path() if save_dir is None else save_dir
        os.makedirs(save_dir, exist_ok=True)
        super().__init__(api_name, save_dir=save_dir,*args, **kwargs)

    def get_stock_list_by_type(self, params, filter_param=None, config=None):
        """获取stock list"""
        base_url = config["base_url"]
        if filter_param:
            params['filter'] = filter_param
        res = self._execute(url=base_url, params=params)
        return res

    def get_stock_list(self, *args, **kwargs):
        """获取全部股票信息"""
        config = kwargs.get('config', WZW_COMMON_STOCK_LIST_API)
        params = kwargs.get('params')
        code_convert = kwargs.get('code_convert', True)
        assert config and params
        infos = {}
        type_ids = params.get('type')
        type_mapping = reverse_dict(config.get('type'))

        if isinstance(type_ids, list):
            type_ids = [int(x) for x in type_ids]
            type_mapping = {type_mapping[x]:x for x in type_ids}
        else:
            type_mapping = {type_mapping.get(type_ids): type_ids}

        for type_str, type_id in type_mapping.items():
            sheet_name = type_str
            params['type'] = type_id
            res = self.get_stock_list_by_type(params=params, config=config)
            res = self._item2dict(self._data_wrapper(res, WZWStockItem))
            # res = list(filter(lambda x: x['bk']==bk and x['stype'] in [1, 2], res))
            if SAVE_DB:
                self.mysql_utils.insert_stock_list_data_to_db(items=res)
            if code_convert:
                res = self.type2str(res)
            infos[sheet_name] = res
        return infos

    def _params_wrapper(self, params: Dict):
        """传参装饰"""
        params["token"] = USER_TOKEN
        params["export"] = 1
        return params

    def type2str(self, data: List[Dict]):
        """stype to name"""
        for item in data:
            if 'stype' in data[0].keys():
                item['stype'] = WZW_STOCK_TYPE.get(
                    item['stype'], item['stype'])
            if 'hsgt' in data[0].keys():
                item['hsgt'] = WZW_HSGT_TYPE.get(item['hsgt'], item['hsgt'])
        # 处理key
        for item in data:
            keys = list(item.keys())
            for k in keys:
                item[WZW_NAME_TYPE.get(k, k)] = item.pop(k)
        return data

    def _execute(self, url: str, params: Dict):
        """执行数据获取"""
        params = self._params_wrapper(params)
        data = super()._execute(url, params)
        return data

    def get_real_time_data(self, *args, **kwargs):
        """获取当日收盘后的实时数据信息"""
        config = kwargs.get('config', WZW_SSHQ_STOCK_DATA_API)
        params = kwargs.get('params')
        analyzer = kwargs.get('analyzer')
        assert config and params
        infos = {}
        type_ids = params.get('type')
        type_mapping = reverse_dict(config.get('type'))

        if isinstance(type_ids, list):
            type_ids = [int(x) for x in type_ids]
            type_mapping = {type_mapping[x]:x for x in type_ids}
        else:
            type_mapping = {type_mapping.get(type_ids): type_ids}
        for type_str, type_id in type_mapping.items():
            sheet_name = type_str
            params['type'] = type_id
            res = self._get_now_data(config=config, params=params)
            res = self._item2dict(self._data_wrapper(
                res, item_class=WZWSSHQDataItem))
            res = self.filter_data(res)
            analysis_res = self.analysis(analyzer=analyzer, infos=res)
            res = self.type2str(res)
            infos[sheet_name] = res
            infos.update(analysis_res)
            # infos[f'{type_str}_今日涨停'] = zt_stocks
            # infos[f'{type_str}_昨日涨停今日表现'] = yestdate_zt_stocks
        return infos

    def visual(self, infos: Dict, viewer: BaseViewer):
        """可视化"""
        viewer.visual(infos)

    def _get_now_data(self, filter_param=None, config=None, params=None):
        """获取当天收盘行情"""
        base_url = config.get('base_url')
        if filter_param:
            params['filter'] = filter_param
        res = self._execute(url=base_url, params=params)
        return res

    def get_minute_k_line(self, codes:List, *args, **kwargs):
        """根据股票列表获取分钟线数据"""
        assert codes and len(codes)>0
        config = kwargs.get('config', WZW_COMMON_K_MINUTE_DATA_API)
        params = kwargs.get('params')
        codes_params = []
        code_param = []
        for code in codes:
            if len(code_param)==50:
                codes_params.append(','.join(code_param))
                code_param = []
            else:
                code_param.append(code)
        codes_params.append(','. join(code_param))
        base_url = config.get('base_url')
        for code in codes_params:
            params['code'] = code
            res =self._execute(url=base_url, params=params)
            res = self._item2dict(self._data_wrapper(res, WZWKMinuteDataItem))
        return res

    def get_hour_k_line(self, codes:List, *args, **kwargs):
        """根据股票列表获取小时线数据"""
        assert codes and len(codes)>0
        config = kwargs.get('config', WZW_COMMON_K_HOUR_DATA_API)
        params = kwargs.get('params')
        codes_params = []
        code_param = []
        for code in codes:
            if len(code_param)==50:
                codes_params.append(','.join(code_param))
                code_param = []
            else:
                code_param.append(code)
        codes_params.append(','. join(code_param))
        base_url = config.get('base_url')
        for code in codes_params:
            params['code'] = code
            res =self._execute(url=base_url, params=params)
            res = self._item2dict(self._data_wrapper(res, WZWKHourDataItem))
        return res

    def get_day_k_line(self, codes:List, *args, **kwargs):
        """根据股票列表获取日线数据"""
        assert codes and len(codes)>0
        config = kwargs.get('config', WZW_COMMON_K_DAY_DATA_API)
        params = kwargs.get('params')
        codes_params = []
        code_param = []
        for code in codes:
            if len(code_param)==50:
                codes_params.append(','.join(code_param))
                code_param = []
            else:
                code_param.append(code)
        codes_params.append(','. join(code_param))
        base_url = config.get('base_url')
        for code in codes_params:
            params['code'] = code
            res =self._execute(url=base_url, params=params)
            res = self._item2dict(self._data_wrapper(res, WZWKDayDataItem))
        return res


if __name__ == "__main__":
    wzw_exec = WZWExecutor()
    excel_path = os.path.join(
        wzw_exec.save_dir, f'{get_time(template="%Y_%m_%d")}_data_list.xlsx')
    excel_viewer = WZWExcel(save_path=excel_path)
    res = wzw_exec.get_now_stock_list()
    wzw_exec.visual(infos=res, viewer=excel_viewer)
