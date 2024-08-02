"""w执行器"""

from typing import Dict, List
import sys
from pathlib import Path
import os
import dataclasses

sys.path.append(str(Path(__file__).resolve().parents[2]))
from src.engine.base import BaseExecutor
from src.utils.constant import *
from src.items.base_item import *
from src.view.excel import WZWExcel, BaseViewer
from src.utils.common import get_default_output_path, load_json, get_time
from src.items.base_item import StockBaseItem
from src.utils.constant import USER_TOKEN
from src.analysis.data_analysis import WZWDataAnalysis

class WZWExecutor(BaseExecutor):
    "歪枣网数据获取执行器"

    def __init__(self, api_name: str = "WZWAPI", save_dir=None):
        save_dir = get_default_output_path() if save_dir is None else save_dir
        os.makedirs(save_dir, exist_ok=True)
        super().__init__(api_name, save_dir=save_dir)

    def get_stock_list_by_type(self, stock_type=0, filter_param=None):
        """获取stock list"""
        base_url = WZW_COMMON_STOCK_LIST_API["base_url"]
        params = {
            "code": "all",
            "type": stock_type,
            "fields": "all",
        }
        if filter_param:
            params['filter'] = filter_param
        res = self._execute(url=base_url, params=params)
        return res

    def get_stock_list(self, bk='主板'):
        """获取全部股票信息"""
        infos = {}
        for type_str, type_id in WZW_COMMON_STOCK_LIST_API.get('type').items():
            sheet_name = type_str
            res = self.get_stock_list_by_type(type_id)
            res = self._item2dict(self._data_wrapper(res, WZWStockItem))
            res = list(filter(lambda x: x['bk']==bk and x['stype'] in [1, 2], res))
            res = self.type2str(res)
            infos[sheet_name] = res
        return infos
    
    def _data_wrapper(self, data: List[Dict], item_class: StockBaseItem):
        """json映射到实体类"""
        data_list = []
        for item in data:
            data_item = item_class(**item)
            data_list.append(data_item)

        return data_list

    def _item2dict(self, data: List[StockBaseItem]):
        return [dataclasses.asdict(x) for x in data]

    def _params_wrapper(self, params: Dict):
        """传参装饰"""
        params["token"] = USER_TOKEN
        params["export"] = 1
        return params
    
    def type2str(self, data: List[Dict]):
        """stype to name"""
        for item in data:
            if 'stype' in data[0].keys():
                item['stype'] = WZW_STOCK_TYPE.get(item['stype'], item['stype'])
            if 'hsgt' in data[0].keys():
                item['hsgt'] = WZW_HSGT_TYPE.get(item['hsgt'], item['hsgt'])
        #处理key
        for item in data:
            keys = list(item.keys())
            for k in keys:
                item[WZW_NAME_TYPE.get(k, k)] = item.pop(k)
        return data
    
    def filter_data(self, info:List[Dict]):
        """过滤脏数据"""
        if 'zsz' in info[0].keys():
            info = list(filter(lambda x:x['zsz']>0, info))
        return info
    
    def _execute(self, url: str, params: Dict):
        """执行数据获取"""
        params = self._params_wrapper(params)
        data = super()._execute(url, params)
        return data

    def get_now_stock_list(self, bk='主板'):
        """获取当日收盘后的实时数据信息"""
        infos = {}
        for type_str, type_id in WZW_COMMON_STOCK_LIST_API.get('type').items():
            sheet_name = type_str
            res = self._get_now_data(type_id)
            res = self._item2dict(self._data_wrapper(res, item_class=WZWSSHQDataItem))
            res = self.filter_data(res)
            zt_stocks, yestdate_zt_stocks = WZWDataAnalysis.get_zt_data(res)
            res = self.type2str(res)
            infos[sheet_name] = res
            infos['今日涨停'] = zt_stocks
            infos['昨日涨停今日表现'] = yestdate_zt_stocks
        return infos
    
    def visual(self, infos:Dict, viewer:BaseViewer):
        """可视化"""
        viewer.visual(infos)

    def _get_now_data(self, stock_type=0, filter_param=None):
        """获取当天收盘行情"""
        base_url = WZW_SSHQ_STOCK_DATA_API.get('base_url')
        params = {
                "code": "all",
                "type": stock_type,
                "fields": "all",
            }
        if filter_param:
            params['filter'] = filter_param
        res = self._execute(url=base_url, params=params)
        return res


if __name__ == "__main__":
    wzw_exec = WZWExecutor()
    excel_path =os.path.join(wzw_exec.save_dir, f'{get_time(template="%Y_%m_%d")}_data_list.xlsx')
    excel_viewer = WZWExcel(save_path=excel_path)
    res = wzw_exec.get_now_stock_list()
    wzw_exec.visual(infos=res, viewer=excel_viewer)