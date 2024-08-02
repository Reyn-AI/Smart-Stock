from .mysql_utils import *
from src.utils.db_constan import *
from src.utils.password_util import *
import time

class MysqlUserUtil(MySQLUtils):
    def __init__(self, host='localhost', user='root', password='root', database='smart_stock', db_port=3306) -> None:
        super().__init__(host, user, password, database, db_port)
        self._db_connect = self._get_db_connect()
    
    def registry(self,
                user_id,
                 user_name,
                 password,
                 role=0,
                 email='',
                 ):
        """用户注册
        
            ARGS:
              user_id 手机号
              user_name 用户名
              password 密码
              role 角色 0普通用户 1 vip用户 2 管理员
              email 邮箱
        """
        try:
            table_name = 'USER_INFO'
            if not self.exist_table(table_name):
                self.logger.warning(f'{table_name} Not Existed in {self.database}.')
                self.create_table(CREATE_TABLE_USER_INFO_SQL)
            password = encrypt_password(password)
            select_sql = SELECT_USER_INFO_SQL.format(user_id) 
            exist_res = self.select(select_sql)
            if exist_res is not None and len(exist_res)>0:
                return False, '用户已存在！'           
            sql = INSERT_USER_INFO_SQL.format(user_id,
                                            password,
                                            user_name,
                                            email,
                                            role
                                            )
            self.logger.info(sql)
            with self.db_connect.cursor() as cursor: 
                res = cursor.execute(sql)
                self.db_connect.commit()
            if res==1:
                return True, '注册成功'
            else:
                return False, '注册失败'
        except Exception as e:
            print(e)
            return False, str(e)
    
    def login(self,
              user_id,
              password):
        """登录"""
        try:
            password = encrypt_password(password)
            sql = CONFIRM_USER_PASSWD_SQL.format(user_id, password)
            result = self.select(sql)
            if result is not None and len(result)>0:
                return True, '登录成功'
            else:
                return False, '密码或用户名不存在!'
        except Exception as e:
            return False, str(e)
    
    def reset_password(self,
                       user_id,
                       password,
                       new_password):
        confirm_res, msg = self.login(user_id=user_id, password=password)
        if not confirm_res:
            return False, '密码验证失败!'
        sql = RESET_USER_PASSWD_SQL.format(encrypt_password(new_password), user_id)
        self.logger.info(sql)
        with self.db_connect.cursor() as cursor: 
            cursor.execute(sql)
            self.db_connect.commit()
        time.sleep(1)
        confirm_res, msg = self.login(user_id=user_id, password=new_password)
        if confirm_res:
            return True, '修改成功'
        else:
            return False, '未知错误'