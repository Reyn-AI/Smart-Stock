from src.utils.common import *
import abc

class HistoryBaseAnalysis(abc.ABC):
    """历史数据选股基类"""
    def __init__(self, *args, **kwargs):
        self.kwargs = kwargs
        self.market = kwargs.get('market', [1,2])
        self.filter_codes = []
        for code in self.market if self.market is not None else [0, 1]:
            if str(code) == '1':
                self.filter_codes.append('0') #深证
            if str(code) == '2':
                self.filter_codes.append('60') #上证
            if str(code) == '3':
                self.filter_codes.extend(['8', '4']) #北证
            if str(code) == '4': #创业板
                self.filter_codes.extend(['30'])
            if str(code) == '5': #科创
                self.filter_codes.append('68')
        self.logger = get_logger()
        self.set_params(**kwargs)
        
    def set_params(self, **kwargs):
        params = kwargs.get('params',[])
        for param in params:
            setattr(self, param['code'], param.get('default'))


class BaseAnalysis(object, metaclass=abc.ABCMeta):
    """数据分析基类"""
    def __init__(self, filter_zb=True, *args, **kwargs):
        self.kwargs = kwargs
        self.filter_zb = filter_zb
        self.filter_key = kwargs.get('filter_key', 'ts_code')
        self.market = kwargs.get('market', [0, 1])
        self.init_vars()
        
    def init_vars(self):
        '''将参数加入类变量'''
        params = self.kwargs.get('params')
        if params is not None:
            for param in params:
                if isinstance(param, dict) and param.get('default') is not None:
                    setattr(self, param.get('code'), param.get('default'))
        
    @abc.abstractmethod
    def analysis(self, infos:Union[List[Dict], pd.DataFrame], **kwargs)->Dict:
        """统一执行的分析方法"""
        from src.utils.stock_utils import get_codes_by_zs_code
        if isinstance(infos, pd.DataFrame) and kwargs.get('pd2dict', False):
            #默认转成dict计算，兼容老版本代码后续统一使用pd计算
            infos = dftodict(infos)
        codes = []
        for code in self.market if self.market is not None else [0, 1]:
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
                
        infos = list(filter(lambda x: (x.get(self.filter_key, False) or x.get('code', False)) and (x.get(self.filter_key) or x.get('code')).startswith(tuple(codes)), infos))
        return infos