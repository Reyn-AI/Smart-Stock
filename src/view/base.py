"""viewer基类"""
from typing import Dict, Union
import pandas as pd
import abc

class BaseViewer(object, metaclass=abc.ABCMeta):
    """viewer基类"""
    def __init__(self):
        pass

    @abc.abstractmethod
    def visual(self, infos:Union[Dict, pd.DataFrame], **kwargs):
        """可视化抽象方法"""
