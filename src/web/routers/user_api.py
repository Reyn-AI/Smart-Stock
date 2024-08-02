from pydantic import BaseModel
from src.utils.common import *
from fastapi import APIRouter
from src.database.mysql_user_util import *
from src.utils.constant import *

router = APIRouter()

class UserItem(BaseModel):
    userID: str #用户id
    email: str = ''# email
    userName: str = '' #用户名
    password: str #密码

class LoginItem(BaseModel):
    userID: str
    password: str

class ResetItem(BaseModel):
    userID: str
    password: str
    newPassword: str


@router.post('/user/registry')
async def registry(params:UserItem):
    result = {'code':200, 'msg':'', 'status':1}
    try:
        util = MysqlUserUtil(host=HOST,
                            user=USER,
                            password=PASSWORD,
                            database=DATABASE,
                            db_port=DB_PORT)
        res, msg = util.registry(user_id=params.userID,
                    user_name=params.userName,
                    password=params.password,
                    email=params.email)
        result['status'] = int(res)
        result['msg'] = msg
    except Exception as e:
        result['code'] = 500
        result['msg'] = str(e)
    finally:
        return result

@router.post('/user/login')
async def login(params:LoginItem):
    result = {'code':200, 'msg':'', 'status':1, 'userToken':''}
    try:
        get_logger().info(f"{params.userID}登录系统!")
        util = MysqlUserUtil(host=HOST,
                            user=USER,
                            password=PASSWORD,
                            database=DATABASE,
                            db_port=DB_PORT)
        res, msg = util.login(user_id=params.userID,
                    password=params.password)
        result['status'] = int(res)
        result['msg'] = msg
        result['userToken'] = get_uuid()
    except Exception as e:
        result['code'] = 500
        result['msg'] = str(e)
    finally:
        return result

@router.post('/user/reset_password')
async def reset_password(params:ResetItem):
    result = {'code':200, 'msg':'', 'status':1, 'userToken':''}
    try:
        util = MysqlUserUtil(host=HOST,
                            user=USER,
                            password=PASSWORD,
                            database=DATABASE,
                            db_port=DB_PORT)
        res, msg = util.reset_password(user_id=params.userID,
                    password=params.password,
                    new_password=params.newPassword)
        result['status'] = int(res)
        result['msg'] = msg
        result['userToken'] = get_uuid()
    except Exception as e:
        result['code'] = 500
        result['msg'] = str(e)
    finally:
        return result