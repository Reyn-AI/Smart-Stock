import os
SAVE_DB = os.getenv('SAVE_DB', False)  #每次获取数据时是否存入数据库
SAVE_JSON = os.getenv('SAVE_JSON', False)
SAVE_MOGODB = os.getenv('SAVE_MONGODB', False)

def get_api_type():
    from src.engine import ApiTypeEnum
    API_TYPE = ApiTypeEnum.AKSHARE #默认使用akshare执行器
    return API_TYPE