from src.api import *
from enum import Enum
from src.utils.constant import COMMON_API_TYPE

class ApiTypeEnum(Enum):
    WZW = 0
    AKSHARE = 1
    TUSHARE = 2
    
class ApiExecutor():
    
    def __init__(self,
                api_type:ApiTypeEnum,
                 *args,
                 **kwargs):
        self.api_executor = self._get_executor(api_type=api_type, *args, **kwargs)
    
    
    def _get_executor(self, api_type, *args, **kwargs):
        if api_type == ApiTypeEnum.WZW:
            return WZWExecutor(*args, **kwargs)
        elif api_type == ApiTypeEnum.AKSHARE:
            return AkShareExecutor(*args, **kwargs)
        elif api_type == ApiTypeEnum.TUSHARE:
            return TuShareExecutor(*args, **kwargs)
        else:
            raise NotImplementedError
    
    def execute(self, api_name,  *args, **kwargs):
        assert api_name in COMMON_API_TYPE.keys()
        func = getattr(self.api_executor, f'get_{api_name}')
        res = func(*args, **kwargs)
        return res
            