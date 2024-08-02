
from typing import Dict, List
ANALYSIS_REGISTRY = []
ANALYSIS_REGISTRY_HISTORY = [] #历史数据选股列表
BUY_FACTOR_REGISTRY = []
CLS_REGISTRY_ADDRESS = {} #所有注册函数的地址如果有重名函数则会被覆盖
SELL_FACTOR_REGISTRY = [] #静态在__init__即可初始化为条件
DYNAMIC_BUY_FACTOR_REGISTRY = [] #动态策略 在回测过程中计算的策略 如需要查看当前持仓成本等
DYNAMIC_SELL_FACTOR_REGISTRY = []
BUY_SIZE_STRATEGY_REGISTRY = []  #买入仓位管理策略注册器
SELL_SIZE_STRATEGY_REGISTRY = [] #卖出仓位管理策略


def get_analysis_registry():
    return list(set(ANALYSIS_REGISTRY))

def get_buy_factor_registry():
    return list(BUY_FACTOR_REGISTRY)

def get_sell_factor_registry():
    return list(SELL_FACTOR_REGISTRY)

def get_dynamic_buy_factor_registry():
    return list(DYNAMIC_BUY_FACTOR_REGISTRY)

def get_dynamic_sell_factor_registry():
    return list(DYNAMIC_SELL_FACTOR_REGISTRY)

def get_sell_size_registry():
    return list(SELL_SIZE_STRATEGY_REGISTRY)

def get_buy_size_registry():
    return list(BUY_SIZE_STRATEGY_REGISTRY)


def size_strategy_register(name:str, params:List[Dict]=[], factor_type='all', desc=None):
    """仓位控制策略注册器"""
    def decorator(cls):
        if factor_type == 'buy':
            if cls.__name__ not in [x['code'] for x in BUY_SIZE_STRATEGY_REGISTRY]:
                BUY_SIZE_STRATEGY_REGISTRY.append({'code':cls.__name__, 'name': name, 'params':params, 'desc':desc})
        elif factor_type=='sell':
            if cls.__name__ not in [x['code'] for x in SELL_SIZE_STRATEGY_REGISTRY]:
                SELL_SIZE_STRATEGY_REGISTRY.append({'code':cls.__name__, 'name': name, 'params':params, 'desc':desc})
        else:
            if cls.__name__ not in [x['code'] for x in BUY_SIZE_STRATEGY_REGISTRY]:
                BUY_SIZE_STRATEGY_REGISTRY.append({'code':cls.__name__, 'name': name, 'params':params, 'desc':desc})
            if cls.__name__ not in [x['code'] for x in SELL_SIZE_STRATEGY_REGISTRY]:    
                SELL_SIZE_STRATEGY_REGISTRY.append({'code':cls.__name__, 'name': name, 'params':params, 'desc':desc})
        CLS_REGISTRY_ADDRESS[cls.__name__] = cls
        return cls
    return decorator

def analysis_register(name:str, params:List[Dict]=[]):
    def decorator(cls):
        if cls.__name__ not in [x['code'] for x in ANALYSIS_REGISTRY]:
            ANALYSIS_REGISTRY.append({'code':cls.__name__, 'name': name, 'params':params})
        CLS_REGISTRY_ADDRESS[cls.__name__] = cls
        return cls
    return decorator

def analysis_register_history(name:str, params:List[Dict]=[]):
    """根据历史数据选股注册器"""
    def decorator(cls):
        if cls.__name__ not in [x['code'] for x in ANALYSIS_REGISTRY_HISTORY]:
            ANALYSIS_REGISTRY_HISTORY.append({'code':cls.__name__, 'name': name, 'params':params})
        CLS_REGISTRY_ADDRESS[cls.__name__] = cls
        return cls
    
    return decorator

def factor_register(name:str, params:List[Dict]=[], factor_type='all', desc=None):
    """静态策略因子注册器"""
    def decorator(cls):
        if factor_type == 'buy':
            if cls.__name__ not in [x['code'] for x in BUY_FACTOR_REGISTRY]:
                BUY_FACTOR_REGISTRY.append({'code':cls.__name__, 'name': name, 'params':params, 'desc':desc})
        elif factor_type=='sell':
            if cls.__name__ not in [x['code'] for x in SELL_FACTOR_REGISTRY]:
                SELL_FACTOR_REGISTRY.append({'code':cls.__name__, 'name': name, 'params':params, 'desc':desc})
        else:
            if cls.__name__ not in [x['code'] for x in BUY_FACTOR_REGISTRY]:
                BUY_FACTOR_REGISTRY.append({'code':cls.__name__, 'name': name, 'params':params, 'desc':desc})
            if cls.__name__ not in [x['code'] for x in SELL_FACTOR_REGISTRY]:    
                SELL_FACTOR_REGISTRY.append({'code':cls.__name__, 'name': name, 'params':params, 'desc':desc})
        CLS_REGISTRY_ADDRESS[cls.__name__] = cls
        return cls
    return decorator

def dynamic_factor_register(name:str, params:List[Dict]=[], factor_type='all', desc=None):
    """动态策略因子注册器"""
    def decorator(cls):
        if factor_type == 'buy':
            if cls.__name__ not in [x['code'] for x in DYNAMIC_BUY_FACTOR_REGISTRY]:
                DYNAMIC_BUY_FACTOR_REGISTRY.append({'code':cls.__name__, 'name': name, 'params':params, 'desc':desc})
        elif factor_type=='sell':
            if cls.__name__ not in [x['code'] for x in DYNAMIC_SELL_FACTOR_REGISTRY]:
                DYNAMIC_SELL_FACTOR_REGISTRY.append({'code':cls.__name__, 'name': name, 'params':params, 'desc':desc})
        else:
            if cls.__name__ not in [x['code'] for x in DYNAMIC_BUY_FACTOR_REGISTRY]:
                DYNAMIC_BUY_FACTOR_REGISTRY.append({'code':cls.__name__, 'name': name, 'params':params, 'desc':desc})
            if cls.__name__ not in [x['code'] for x in DYNAMIC_SELL_FACTOR_REGISTRY]:
                DYNAMIC_SELL_FACTOR_REGISTRY.append({'code':cls.__name__, 'name': name, 'params':params, 'desc':desc})
        CLS_REGISTRY_ADDRESS[cls.__name__] = cls
        return cls
    return decorator

CALCULATE_FACTOR_REGISTRY = []
CALCULATE_FACTOR_REGISTRY_DICT = {}
def factor_calculate_register(name:str, must_params:List=['open', 'high', 'low', 'close'], other_params=None, view='overlap', desc=None):
    """因子计算类注册器，注册的因子可以在买卖点分析展示"""
    def decorator(cls):
        if cls.__name__ not in [x['value'] for x in CALCULATE_FACTOR_REGISTRY]:
            CALCULATE_FACTOR_REGISTRY.append({'value':cls.__name__, 'view': view, 'must_params':must_params, 'other_params':other_params, 'label':name, 'desc':desc})
            CALCULATE_FACTOR_REGISTRY_DICT[cls.__name__] = {'value':cls.__name__, 'view': view, 'must_params':must_params, 'other_params':other_params, 'label':name, 'desc':desc}
        CLS_REGISTRY_ADDRESS[cls.__name__] = cls
        return cls
    return decorator