"""枚举类"""
from enum import Enum


class ApiType(Enum):
    """API接口的枚举类"""
    TUSHARE = 0
    WZW = 1
    AKSHARE = 2