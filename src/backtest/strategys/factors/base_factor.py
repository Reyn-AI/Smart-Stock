import abc
from typing import List, Dict, Optional
from src.utils.common import get_logger

class BaseFactor(metaclass=abc.ABCMeta):
    
    def __init__(self, order_type:int) -> None:
        """Args:
            order_type -1卖 1买 用于区分因子中不同逻辑
        """
        self.order_type = order_type
        self.logger = get_logger()
        
    @abc.abstractmethod
    def get_indicator(self, data, *args, **kwargs):
        """获取示例化后的指示器"""
        params = kwargs.get('params', [])
        self.set_params(params)
    
    def set_params(self, params:List[Dict]):
        """设置属性"""
        for param in params:
            code = param.get('code')
            default = param.get('default')
            setattr(self, code, default)


class BaseFactorCalculate(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def call_metric(self, *args, **kwargs):
        pass
    
    async def async_call_metric(self, *args, **kwargs):
        return self.call_metric(*args, **kwargs)