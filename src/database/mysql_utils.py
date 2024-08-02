from typing import List, Dict
import pymysql
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2]))
from src.utils.db_constan import *
from src.utils.common import get_logger, fmt_date
import re
import pandas as pd
import threading
lock = threading.Lock()

CONNECT = None
class MySQLUtils(object):
    def __init__(self,
                 host='localhost',
                 user='root',
                 password='root',
                 database='smart_stock',
                 db_port = 3306
                 ) -> None:
        from src.utils.env import SAVE_DB
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.db_port = db_port
        self.logger = get_logger()
        if SAVE_DB:
            self._db_connect = self._get_db_connect()

    def _get_db_connect(self):
        try:
            connect =  pymysql.connect(host=self.host,
                                   user=self.user,
                                   password=self.password,
                                   database=self.database,
                                   port=self.db_port) if CONNECT is None else CONNECT
            return connect
        except Exception as e:
            self.logger.error(str(e))
            SAVE_DB = False
            return None
    
    @property    
    def exist_conncect(self):
        """判断是否存在db链接"""
        if self.db_connect is None:
            return False
        return True

    @property
    def db_connect(self):
        """获取db链接"""
        return self._db_connect
    
    def exist_table(self, table_name):
        """判断表是否存在"""
        try:
            # 创建游标对象
            if not self.exist_conncect:
                return False
            with self.db_connect.cursor() as cursor:
                # 编写SQL查询语句，检查表是否存在
                sql = f"SHOW TABLES LIKE '{table_name}'"
                lock.acquire()
                # 执行SQL语句
                cursor.execute(sql)
                # 获取查询结果
                result = cursor.fetchone()
                
                # 判断表是否存在
                if result:
                    return True
                else:
                    return False
        except Exception as e:
            self.logger.error(str(e))
        finally:
            if lock.locked():
                lock.release()

    def create_table(self, sql:str):
        """创建表"""
        try:
            table_name = re.findall(r"CREATE TABLE (.*)\w*\(.*", sql)[0]
            if self.exist_table(table_name):
                self.logger.warning(f'{table_name} Existed in {self.database}.')
                return
            self.logger.info(f"Create Table:{sql}.")
            with self.db_connect.cursor() as cursor:
                lock.acquire()
                res = cursor.execute(sql)
            return res
        except Exception as e:
            print(e)
        finally:
            if lock.locked():
                lock.release()

    def insert_stock_list_data_to_db(self, items:List[Dict]):
        """往数据库插入数据"""
        try:
            table_name = 'STOCK_LIST'
            if not self.exist_table(table_name):
                self.logger.warning(F'{table_name} Not Existed in {self.database}.')
                self.create_table(CREATE_K_MIN_DATA_SQL)
            else:
                self.logger.info(f'Insert data to {table_name}')
                SQL_TEMPLATE = INSERT_STOCK_LIST_SQL_TEMPLATE
                with self.db_connect.cursor() as cursor:
                    for item in items:
                        code = item['code']
                        name = item['name']
                        stype = item['stype']
                        hsgt = item['hsgt']
                        bk = item['bk']
                        roe = item['roe']
                        zgb = item['zgb']
                        ltgb = item['ltgb']
                        ltsz = item['ltsz']
                        zsz = item['zsz']
                        ssdate = item['ssdate']
                        z50 = item['z50']
                        z52 = item['z52']
                        z53 = item['z53']
                        exec_sql = SQL_TEMPLATE.format(f'"{code}"', f'"{name}"', stype, hsgt, f"'{bk}'", roe, zgb, ltgb, ltsz, zsz, f"'{ssdate}'", f"'{z50}'", f"'{z52}'", f"'{z53}'")
                        lock.acquire()
                        cursor.execute(exec_sql)
                    self.db_connect.commit()
        except Exception as e:
            self.logger.error(str(e))
        finally:
            if lock.locked():
                lock.release()

    def insert_stock_list_data_to_db(self, items:pd.DataFrame):
        """往数据库插入数据"""
        try:
            table_name = 'K_MIN_DATA'
            if not self.exist_table(table_name):
                self.logger.warning(F'{table_name} Not Existed in {self.database}.')
            else:
                self.logger.info(f'Insert data to {table_name}')
                SQL_TEMPLATE = INSERT_K_MIN_DATA_SQL
                with self.db_connect.cursor() as cursor:
                    for item in items.iterrows():
                        code = item[1].code
                        open = item[1].open
                        high = item[1].high
                        low = item[1].low
                        volume = item[1].volume
                        exec_sql = SQL_TEMPLATE.format(f'"{code}"', f'"{open}"', f'"{high}"', f'"{low}"', f'"{volume}"')
                        lock.acquire()
                        cursor.execute(exec_sql)
                    self.db_connect.commit()
        except Exception as e:
            self.logger.error(str(e))
        finally:
            if lock.locked():
                lock.release()
    
    
    def insert_tushare_real_time_data_to_db(self, items:List[Dict]):
        """往tushare实时数据表插入数据"""
        try:
            table_name = 'TUSHARE_REALTIME_DATA'
            if not self.exist_table(table_name):
                self.logger.warning(F'{table_name} Not Existed in {self.database}.')
                self.create_table(CREATE_TUSHARE_REAL_TIME_DATA_SQL)
            else:
                self.logger.info(f'Insert data to {table_name}')
                SQL_TEMPLATE = INSERT_TUSHARE_REAL_TIME_DATA_SQL
                with self.db_connect.cursor() as cursor:
                    for item in items:
                        trade_date = item.pop('date')
                        trade_time = item.pop('time')
                        date = fmt_date(trade_date) +f' {trade_time}'
                        exec_sql = SQL_TEMPLATE.format(f"'{date}'", f"'{item['ts_code'].split('.')[0]}'", f"'{item['name']}'", item['open'],
                                                       item['pre_close'], item['price'], item['high'], item['low'], item['volume'],
                                                        item['amount'], item['bid'], item['ask'], item['b1_v'], item['b1_p'],
                                                        item['b2_v'], item['b2_p'], item['b3_v'], item['b3_p'],
                                                        item['b4_v'], item['b4_p'], item['b5_v'], item['b5_p'],
                                                        item['a1_v'], item['a1_p'], item['a2_v'], item['b2_p'],
                                                        item['a3_v'], item['a3_p'], item['a4_v'], item['a4_p'],
                                                        item['a5_v'], item['a5_p'])
                        cursor.execute(exec_sql)
                    self.db_connect.commit()
        except Exception as e:
            self.logger.error(str(e))


    def select(self, sql):
        """查询"""
        if self.db_connect is None:
            return None
        try:
            with self.db_connect.cursor() as cursor:
                lock.acquire()
                cursor.execute(sql)
                results = cursor.fetchall()
                    # 打印结果
            return results
        except Exception as e:
            print(e)
        finally:
            if lock.locked():
                lock.release()
    
    def select_real_time_data(self, where=None):
        """根据where查找数据"""
        # SQL 查询语句
        sql = f"SELECT * FROM TUSHARE_REALTIME_DATA"
        if where:
            sql += f" WHERE {where}"
        results = self.select(sql)
        res = []
        for item in results:
            res.append({
                'date':item[0].isoformat(), 'ts_code':item[1], 'name':item[2], 'open':item[3], 'pre_close':item[4],
                'price':item[5], 'high':item[6], 'low':item[7], 'volumn':item[8], 'amount':item[9], 'bid':item[10],
                'ask':item[11], 'b1_v':item[12], 'b1_p':item[13], 'b2_v':item[14], 'b2_p':item[15], 'b3_b':item[16],
                'b3_p':item[17], 'b4_v':item[18], 'b4_p':item[19], 'b5_v':item[20], 'b5_p':item[21], 'a1_b':item[22],
                'a1_p':item[23], 'a2_v':item[24], 'a2_p':item[25], 'a3_v':item[26], 'a3_p':item[27],
                'a4_v':item[28], 'a4_p':item[29], 'a5_v':item[30], 'a5_p':item[31]
            })
        return res

    def select_stock_list(self, where=None):
        """根据where查找数据"""
        # SQL 查询语句
        sql = f"SELECT * FROM STOCK_LIST"
        if where:
            sql += f" WHERE {where}"
        results = self.select(sql)
        res = []
        for item in results:
            code = item[0]
            name = item[1]
            stype = item[2]
            hsgt = item[3]
            bk = item[4]
            roe = item[5]
            zgb = item[6]
            ltgb = item[7]
            ltsz = item[8]
            zsz = item[9]
            ssdate = item[10].isoformat()
            z50 = item[11]
            z52 = item[12]
            z53 = item[13]
            res.append({
                'code':code,
                'name':name,
                'stype':stype,
                'hsgt':hsgt,
                'bk':bk,
                'roe':roe,
                'zgb':zgb,
                'ltgb':ltgb,
                'ltsz':ltsz,
                'zsz':zsz,
                'ssdate':ssdate,
                'z50':z50,
                'z52':z52,
                'z53':z53
            })
        return res

    def close(self):
        """关闭数据库链接"""
        self.db_connect.close()        

# if __name__ == '__main__':
#     create_table = CREATE_TUSHARE_REAL_TIME_DATA_SQL
#     MySQLUtils().select_real_time_data()