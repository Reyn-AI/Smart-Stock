from src.database.mysql_user_util import *
from src.utils.db_constan import *

utils = MysqlUserUtil(host=HOST,
                      user=USER,
                      password=PASSWORD,
                      database=DATABASE,
                      db_port=DB_PORT)

def test_registry():
    res = utils.registry('19850160511',
                   'liqy',
                   'test12345',
                   role='2',
                   email='smart-stock@163.com')
    print(res)

def test_login():
    res = utils.login(user_id='19850160511',
                      password='test12345')
    print(res)


def test_reset_password():
    res = utils.reset_password(user_id='19850160511',
                               password='test12345',
                               new_password='smart-stock')
    print(res)

test_reset_password()