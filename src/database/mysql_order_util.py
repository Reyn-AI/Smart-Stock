from .mysql_utils import *
from src.utils.db_constan import *
from src.utils.password_util import *
import time
from src.utils.common import *
import threading
lock = threading.Lock()

class MysqlOrderUtil(MySQLUtils):
    def __init__(self,
                 host=HOST,
                 user=USER,
                 password=PASSWORD,
                 database=DATABASE,
                 db_port=DB_PORT) -> None:
        super().__init__(host, user, password, database, db_port)
        self._db_connect = self._get_db_connect()
        self.json_util = LoadJsonInfo()
    
    def add_order(self,
                user_id,
                stock_name,
                trade_date,
                volume,
                price,
                stockStatus
                 ):
        """新增交割单
            ARGS:
              user_id 手机号
              stock_name 股票名
              trade_date 交易日期
              volume 成交量
              price 成交价格
              stockStatus 买/卖 0/1
        """
        try:
            table_name = 'ORDER_INFO'
            if not self.exist_table(table_name):
                self.logger.warning(f'{table_name} Not Existed in {self.database}.')
                self.create_table(CREATE_TABLE_ORDER_INFO_SQL)
            if not self.json_util.stock_name_exist(stock_name):
                return False, '股票名称不存在'
            code = self.json_util.get_code_by_name(stock_name)
            account = volume*price
            sql = INSERT_ORDER_INFO_SQL.format(user_id,
                                            stock_name,
                                            code,
                                            trade_date,
                                            volume,
                                            account,
                                            price,
                                            stockStatus
                                            )
            self.logger.info(sql)
            with self.db_connect.cursor() as cursor: 
                lock.acquire()
                res = cursor.execute(sql)
                self.db_connect.commit()
            if res==1:
                return True, '添加成功'
            else:
                return False, '添加失败'
        except Exception as e:
            print(e)
            return False, str(e)
        finally:
            if lock.locked():
                lock.release()
    
    def select_order(self,
                user_id,
                stock_name=None,
                 ):
        try:
            results = []
            if stock_name is None:
                sql = SELECT_ORDER_INFO_ALL_SQL.format(user_id)
            else:
                sql = SELECT_ORDER_INFO_SQL.format(user_id, stock_name)
            self.logger.info(sql)
            result = self.select(sql)
            if result is not None and len(result)>0:
                for item in result:
                    results.append({
                        'id':item[0],
                        '股票名': item[1],
                        '代码': item[2],
                        '交易日期':item[3].strftime("%Y-%m-%d %H:%M:%S"),
                        '价格': item[4],
                        '成交量(股)':item[5],
                        '成交额':item[6],
                        '状态':'buy' if item[7]==0 else 'sell'
                    })
            return results, '查询成功'
        except Exception as e:
            print(e)
            return results, str(e)
            
    def update_order(self,
                     user_id,
                     id,
                     stock_name,
                     trade_date,
                     volume,
                     price,
                     stock_status):
        try:
            code = self.json_util.get_code_by_name(stock_name)
            account = volume * price
            sql = UPDATE_ORDER_INFO_SQL.format(stock_name,
                                               code,
                                               trade_date,
                                               volume,
                                               account,
                                               price,
                                               stock_status,
                                               id,
                                               user_id)
            self.logger.info(sql)
            with self.db_connect.cursor() as cursor: 
                lock.acquire()
                res = cursor.execute(sql)
                self.db_connect.commit()
            if res==1:
                return True, '更新成功'
            else:
                return False, '更新失败'
        except Exception as e:
            print(e)
            return False, str(e)
        finally:
            if lock.locked():
                lock.release()
    
    def delete_order(self,
                    user_id,
                    id):
        try:
            
            sql = DELETE_ORDER_INFO_SQL.format(id, user_id)
            with self.db_connect.cursor() as cursor: 
                lock.acquire()
                res = cursor.execute(sql)
                self.db_connect.commit()
            if res==1:
                return True, '删除成功'
            else:
                return False, '删除失败'
        except Exception as e:
            print(e)
            return False, str(e)
        finally:
            if lock.locked():
                lock.release()
    
    def select_order_and_sum(self,
                             user_id,
                            stock_name=None):
        """查询并汇总"""
        try:
            results, _= self.select_order(user_id=user_id,
                                        stock_name=stock_name)
            sum_results = {}
            for res in results:
                name = res['股票名']
                status = -1 if res['状态']=='sell' else 1
                volume = res['成交量(股)']
                account = res['成交额']
                if name not in sum_results.keys():
                    sum_results[name] = res
                else:
                    volume = sum_results[name]['成交量(股)'] + status*volume
                    account = sum_results[name]['成交额'] + account * status
                    sum_results[name]['价格'] = round(account/volume, 2) if volume != 0 else 0
                    sum_results[name]['成交量(股)'] = volume
                    sum_results[name]['成交额'] = account
                    if volume ==0:
                        sum_results[name]['状态'] = 'empty'
                
            return list(sum_results.values()), '查询成功'
        except Exception as e:
            print(e)
            return results, str(e)