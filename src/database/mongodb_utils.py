
from typing import Dict, List
from src.utils.db_constan import *
from src.utils.common import *
import pymongo
import time
from src.utils.env import get_api_type

class MongoDBUtil:
    def __init__(self,
                 ip:str=MONGODB_IP,
                 port:int=MONGODB_PORT):
        self.URL = f'mongodb://{MONGODB_USER}:{MONGODB_PWD}@{ip}:{port}'
        self.client = None
        self.logger = get_logger()
    
    def _get_connection(self):
        """获取db链接"""
        try:
            if self.client is None:
                self.client = pymongo.MongoClient(self.URL, connectTimeoutMS=100)
                db = self.client.smart_stock
                db.command('ping')
                time.sleep(0.01)
        except Exception as e:
            self.logger.warning(str(e))
        return self.client
    
    def _get_db(self, name=MONGODB_NAME):
        if self.client is None:
            self.client = self._get_connection()
            if self.client is None:
                return None
        return self.client[name]

    def _get_collection(self, name):
        db = self._get_db()
        if db is None:
            return None
        return db[name]
    
    async def insert_real_time_data(self, data:List[Dict],col_name:str=REALTIME_COLLECTION_NAME, id=None):
        """查入每天的实时数据固定id是当日日期"""
        try:
            id = get_time(template='%Y-%m-%d') if id is None else id
            datetime = get_time()
            collection = self._get_collection(col_name)
            data = {'data':data, '_id':id, 'datetime':datetime}
            res = collection.insert_one(data)
        except Exception as e:
            if 'duplicate key' in str(e):
                collection.delete_one({'_id':data['_id']})
                collection.insert_one(data)
                self.logger.warning(f'insert_one exist duplicate key, delete and update!')
            return False
        return res
    
    async def get_real_time_data(self, col_name=REALTIME_COLLECTION_NAME, id=get_time('%Y-%m-%d'), force_update=False, auto_get=True):
        """获取实时数据"""
        try:
            from src.engine  import ApiExecutor
            collection = self._get_collection(col_name)
            if collection is None:
                return []
            res = collection.find_one({'_id':id})
            codes = get_all_stock_codes()
            params = {'ts_code':codes, 'src':'sina'}
            if auto_get and res is None or force_update:

                res = ApiExecutor(api_type=get_api_type()).execute('real_time_data', params=params)
                if res is not None:
                    await self.insert_real_time_data(res, id=id)
                return res
            else:
                if res is not None:
                    if len(res['data'])==0:
                        res = ApiExecutor(api_type=get_api_type()).execute('real_time_data', params=params)
                        if res is not None:
                            await self.insert_real_time_data(res, id=id)
                            return res
                return res['data']
        except Exception as e:
            self.logger.error(str(e))
        
    def insert_backtrader_record(self, 
                                 data:Dict,
                                 col_name:str=BACKTRADE_RECODE_COLLECTION_NAME):
        """插入回测记录"""
        try:
            data['_id'] = get_uuid()
            collection = self._get_collection(col_name)
            res = collection.insert_one(data)
        except Exception as e:
            self.logger.warning(f'insert_one upload Failed!{str(e)}')
            return False
        return res
    
    def delete_backtrader_record(self, id, col_name:str=BACKTRADE_RECODE_COLLECTION_NAME):
        """删除回测记录"""
        try:
            collection = self._get_collection(col_name)
            res = collection.delete_one({"_id": id})
        except Exception as e:
            self.logger.warning(f'insert_one upload Failed!{str(e)}')
            return False
        return res
        
    def get_backtrader_record_data(self, user_id, col_name=BACKTRADE_RECODE_COLLECTION_NAME):
        """获取回测记录"""
        try:
            collection = self._get_collection(col_name)
            if collection is None:
                return []
            res = collection.find({'userID':user_id},
                                  { "_id": 1,
                                   "recordName": 1,
                                   'datetime':1,
                                   'returnsTable':1,
                                   'defaultParams':1,
                                   'buyStrategys':1,
                                   'sellStrategys':1,
                                   'buySizeStrategys':1,
                                   'sellSizeStrategys':1,
                                   'buyCombineType':1,
                                   'sellCombineType':1,
                                   'orderStockNames':1})
            res = [x for x in res]
            if res is None:
                res = []
        except Exception as e:
            self.logger.error(str(e))
        finally:
            return res
        
    def get_backtrader_record_data_by_id(self, id, col_name=BACKTRADE_RECODE_COLLECTION_NAME):
        """通过id获取完整的回测记录"""
        try:
            collection = self._get_collection(col_name)
            if collection is None:
                return {}
            res = collection.find({'_id':id})
            if res is None:
                res = {}
            res = [x for x in res]
            if len(res)>0:
                res = res[0]
        except Exception as e:
            self.logger.error(str(e))
        finally:
            return res

if __name__ == '__main__':
    res = MongoDBUtil().get_backtrader_record_data(user_id='19850160511')
    breakpoint()