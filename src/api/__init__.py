"""数据获取接口网关"""
from .tushare_executor import TuShareExecutor
from .akshare_executor import AkShareExecutor
from .wzw_executor import WZWExecutor

__all__ = ['TuShareExecutor', 'AkShareExecutor', 'WZWExecutor']