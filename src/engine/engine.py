"""执行引擎"""
from pathlib import Path
import os
import sys

sys.path.append(str(Path(__file__).resolve().parents[2]))
from src.api.base import BaseExecutor
from src.view.base import BaseViewer
from src.utils.common import *
from src.utils.env import get_api_type

class Engine:
    """执行层"""

    def __init__(self,
                 api: BaseExecutor=None,
                 viewers:List[BaseViewer]=None):
        self.api = api
        self.viewers = viewers

    def execute(self, api_name, *args, **kwargs):
        """web执行"""
        from src.engine import ApiExecutor
        api_executor = ApiExecutor(api_type=get_api_type())
        res = api_executor.execute(api_name=api_name, *args, **kwargs)
        if self.viewers and not isinstance(self.viewers, list):
            self.viewers = [self.viewers]
        if self.viewers and len(self.viewers)>0:
            for viewer in self.viewers:
                viewer.visual(res, *args, **kwargs)
        return res
    
    def run(self, api_type:str, *args, **kwargs):
        """执行"""
        res = self.api.get_data_from_api(api_type=api_type, *args, **kwargs)
        if self.viewers and not isinstance(self.viewers, list):
            self.viewers = [self.viewers]
        if self.viewers and len(self.viewers)>0:
            for viewer in self.viewers:
                viewer.visual(res, *args, **kwargs)
        return res

    def add_viewer(self, viewer:BaseViewer):
        """添加可视化"""
        self.viewer = viewer

if __name__ == '__main__':
    from src.api.wzw_executor import WZWExecutor
    from src.view.excel import WZWExcel
    api = WZWExecutor()
    excel_path = os.path.join(
        api.save_dir, f'{get_time(template="%Y_%m_%d")}_data_list.xlsx')
    excel_viewer = WZWExcel(save_path=excel_path)
    engine = Engine(api=api, viewer=excel_viewer)
    engine.run(api_type='stock_list')