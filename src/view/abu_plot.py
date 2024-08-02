from typing import Dict, Union
from abupy import ABuSymbolPd
from abupy import tl
from pandas import DataFrame
from src.utils.common import *
from src.view.base import BaseViewer

class LineViewer(BaseViewer):
    
    def __init__(self, **kwargs):
        self.how = kwargs.get('how', 'both')
        
    def visual(self, infos: Union[Dict, DataFrame], *args, **kwargs):
        infos = infos.get('plot')
        if infos:
            if isinstance(infos, list):
                infos = tushare_dict_to_df(infos)
            symbols = infos.ts_code.to_list()
            for symbol in symbols:
                self.plot_trend(symbol, how=self.how)
                
    def plot_trend(self, symbol, n_folds=1, only_last=True, how='both', show_step=False, output_dir=None, **kwargs):
        symbol = code_to_abu_code(symbol)
        if output_dir is None:
            output_dir = os.path.join(get_default_output_path(), f'trend/{symbol}')
            os.makedirs(output_dir, exist_ok=True)
            os.environ['OUTPUT_DIR'] = output_dir
        n_folds = int(n_folds)
        # 获取symbol的n_folds年数据
        kl = ABuSymbolPd.make_kl_df(symbol, n_folds=n_folds)
        # 构造技术线对象
        kl_tl = tl.AbuTLine(kl.close, 'kl', code=symbol)
        if how=='all' or 'support' in how:
            # 只绘制支持线
            res = kl_tl.show_support_trend(only_last=only_last, show=True, show_step=show_step)
        if how=='all' or 'resistance' in how:
            # 只绘制阻力线
            res = kl_tl.show_resistance_trend(only_last=only_last, show=True, show_step=show_step)
        if how=='all' or 'both' in how:
            # 支持线和阻力线都绘制
            res=kl_tl.show_support_resistance_trend(only_last=only_last, show=True, show_step=show_step)
        if how=='all' or 'jump' in how:
            res = tl.jump.calc_jump(kl, show=True, jump_diff_factor=kwargs.get('jump_diff_factor', 0.8))
        if how=='all' or 'jump_line' in how:
            res = tl.jump.calc_jump_line(kl, show=True, jump_diff_factor=kwargs.get('jump_diff_factor', 0.5))
        if how=='all' or 'trend' in how:
            res = kl_tl.show_regress_trend_channel()
        del os.environ['OUTPUT_DIR']
        return res

    

if __name__ == '__main__':
    LineViewer().plot_trend('600640', how='trend')