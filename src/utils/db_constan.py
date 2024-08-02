"""Mysql 配置"""
import os
# HOST="139.159.177.235"
HOST=os.getenv('MYSQL_HOST', '60.204.132.107')
USER=os.getenv("MYSQL_USER", 'root')
PASSWORD=os.getenv("MYSQL_PASSWORD", "smart-stock")
DATABASE=os.getenv("MYSQL_DB_NAME","smart_stock")
# DB_PORT = 3308
DB_PORT = os.getenv("MYSQL_DB_PORT", 3306)
CREATE_TABLE_STOCK_LIST_SQL =  """CREATE TABLE STOCK_LIST (
                            CODE  CHAR(20) PRIMARY KEY,
                            NAME  CHAR(20),
                            STYPE INT,  
                            HSGT INT,
                            BK CHAR(20),
                            ROE FLOAT,
                            ZGB FLOAT,
                            LTGB FLOAT,
                            LTSZ FLOAT,
                            ZSZ FLOAT,
                            SSDATE DATETIME,
                            Z50 CHAR(100),
                            Z52 CHAR(100),
                            Z53 TEXT,
                              )"""  #创建歪枣网股票基本信息表

INSERT_STOCK_LIST_SQL_TEMPLATE = """
                                INSERT INTO STOCK_LIST(CODE, NAME, STYPE, HSGT, BK, ROE, ZGB, LTGB, LTSZ, ZSZ, SSDATE, Z50, Z52, Z53) 
                                VALUES({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}) ON DUPLICATE KEY UPDATE
                                NAME=VALUES(NAME),
                                STYPE=VALUES(STYPE),
                                HSGT=VALUES(HSGT),
                                BK=VALUES(BK),
                                ROE=VALUES(ROE),
                                ZGB=VALUES(ZGB),
                                LTGB=VALUES(LTGB),
                                LTSZ=VALUES(LTSZ),
                                ZSZ=VALUES(ZSZ),
                                SSDATE=VALUES(SSDATE),
                                Z50=VALUES(Z50),
                                Z52=VALUES(Z52),
                                Z53=VALUES(Z53)
                            """ #插入股票基本信息模板

INSERT_TUSHARE_REAL_TIME_DATA_SQL = """
                                INSERT INTO TUSHARE_REALTIME_DATA (
                                    DATE, CODE, NAME, OPEN,PRE_CLOSE, PRICE, HIGH, LOW, VOLUME, AMOUNT, BID,
                                    ASK, B1_V, B1_P, B2_V, B2_P, B3_V, B3_P, B4_V, B4_P, B5_V, B5_P, A1_V, A1_P, A2_V, A2_P, A3_V,
                                    A3_P, A4_V, A4_P, A5_V, A5_P
                              ) VALUES({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {},
                                       {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}) ON DUPLICATE KEY UPDATE
                                DATE=VALUES(DATE), NAME=VALUES(NAME), CODE=VALUES(CODE), OPEN=VALUES(OPEN), PRE_CLOSE=VALUES(PRE_CLOSE),
                                PRICE=VALUES(PRICE), HIGH=VALUES(HIGH), LOW=VALUES(LOW), VOLUME=VALUES(VOLUME), AMOUNT=VALUES(AMOUNT),
                                BID=VALUES(BID), ASK=VALUES(ASK), B1_V=VALUES(B1_V), B1_P=VALUES(B1_P), B2_V=VALUES(B2_V),
                                B2_P=VALUES(B2_P), B3_V=VALUES(B3_V), B3_P=VALUES(B3_P), B4_V=VALUES(B4_V), B4_P=VALUES(B4_P),
                                B5_V=VALUES(B5_V), B5_P=VALUES(B5_P), A1_V=VALUES(A1_V), A1_P=VALUES(A1_P), A2_V=VALUES(A2_V),
                                A2_P=VALUES(A2_P), A3_V=VALUES(A3_V), A3_P=VALUES(A3_P), A4_V=VALUES(A4_V), A4_P=VALUES(A4_P),
                                A5_V=VALUES(A5_V),A5_P=VALUES(A5_P)
                            """

CREATE_TUSHARE_REAL_TIME_DATA_SQL = """
                                CREATE TABLE TUSHARE_REALTIME_DATA (
                                    DATE DATETIME,
                                    CODE  CHAR(20),
                                    NAME  CHAR(20),
                                    OPEN FLOAT,  
                                    PRE_CLOSE FLOAT,
                                    PRICE FLOAT,
                                    HIGH FLOAT,
                                    LOW FLOAT,
                                    VOLUME INT,
                                    AMOUNT FLOAT,
                                    BID FLOAT,
                                    ASK FLOAT,
                                    B1_V FLOAT,
                                    B1_P FLOAT,
                                    B2_V FLOAT,
                                    B2_P FLOAT,
                                    B3_V FLOAT,
                                    B3_P FLOAT,
                                    B4_V FLOAT,
                                    B4_P FLOAT,
                                    B5_V FLOAT,
                                    B5_P FLOAT,
                                    A1_V FLOAT,
                                    A1_P FLOAT,
                                    A2_V FLOAT,
                                    A2_P FLOAT,
                                    A3_V FLOAT,
                                    A3_P FLOAT,
                                    A4_V FLOAT,
                                    A4_P FLOAT,
                                    A5_V FLOAT,
                                    A5_P FLOAT
                              );
                            """


CREATE_K_MIN_DATA_SQL = """
                                CREATE TABLE K_MIN_DATA (
                                    DATE DATETIME,
                                    CODE  CHAR(20),
                                    OPEN FLOAT,  
                                    HIGH FLOAT,
                                    LOW FLOAT,
                                    CLOSE FLOAT,
                                    VOLUME INT
                              );
                            """
INSERT_K_MIN_DATA_SQL = """
                                INSERT INTO K_MIN_DATA (
                                    DATE, CODE, NAME, OPEN,HIGH, LOW, CLOSE, VOLUME
                              ) VALUES({}, {}, {}, {}, {}, {}, {}) ON DUPLICATE KEY UPDATE
                                DATE=VALUES(DATE), CODE=VALUES(CODE), OPEN=VALUES(OPEN), HIGH=VALUES(HIGH), LOW=VALUES(LOW), VOLUME=VALUES(VOLUME),CLOSE=VALUES(CLOSE);
                            """


CREATE_TABLE_USER_INFO_SQL =  """CREATE TABLE USER_INFO (
                            USERID  CHAR(20) PRIMARY KEY,
                            PASSWORD CHAR(100),
                            NAME  CHAR(20),
                            EMAIL CHAR(20),  
                            ROLE INT DEFAULT 0,
                            STATUS INT DEFAULT 0
                              );"""  #创建用户信息表

SELECT_USER_INFO_SQL = """
                    SELECT *FROM USER_INFO WHERE USERID='{}' AND STATUS=0;
                    """ #查看用户是否已经注册

INSERT_USER_INFO_SQL = """
                      INSERT INTO USER_INFO(USERID, PASSWORD, NAME, EMAIL, ROLE) 
                                VALUES('{}', '{}', '{}', '{}', {});

                      """ #用户注册
CONFIRM_USER_PASSWD_SQL = """SELECT *FROM USER_INFO WHERE USERID='{}' AND PASSWORD='{}' AND STATUS=0;"""  #验证密码

RESET_USER_PASSWD_SQL = """
                      UPDATE USER_INFO SET PASSWORD='{}' WHERE USERID='{}' AND STATUS=0;
                    """ #重置密码

CREATE_TABLE_ORDER_INFO_SQL = """
                              CREATE TABLE ORDER_INFO(
                                ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                USERID CHAR(20),
                                STOCK_NAME CHAR(20),
                                CODE CHAR(20),
                                TRADE_DATE DATETIME,
                                VOLUME INT,
                                ACCOUNT FLOAT,
                                PRICE FLOAT,
                                STOCK_STATUS int,
                                STATUS int DEFAULT 0
                              )
                          """ #创建交割单表

INSERT_ORDER_INFO_SQL = """
                      INSERT INTO ORDER_INFO (
                                    USERID, STOCK_NAME, CODE, TRADE_DATE, VOLUME, ACCOUNT, PRICE, STOCK_STATUS
                              ) VALUES('{}', '{}', '{}', '{}', {}, {}, {}, {}) ON DUPLICATE KEY UPDATE
                                USERID=VALUES(USERID), STOCK_NAME=VALUES(STOCK_NAME),
                                CODE=VALUES(CODE), TRADE_DATE=VALUES(TRADE_DATE),
                                VOLUME=VALUES(VOLUME), ACCOUNT=VALUES(ACCOUNT),
                                PRICE=VALUES(PRICE), STOCK_STATUS=VALUES(STOCK_STATUS);
                      """ #新增交割单
UPDATE_ORDER_INFO_SQL = """
                    UPDATE ORDER_INFO SET STOCK_NAME='{}', CODE='{}', TRADE_DATE='{}', VOLUME={},
                                      ACCOUNT={}, PRICE={}, STOCK_STATUS={}
                    WHERE ID={} AND USERID={} AND STATUS=0;
                    """#修改交割单

SELECT_ORDER_INFO_SQL = """
                    SELECT ID, STOCK_NAME, CODE, TRADE_DATE, PRICE, VOLUME, ACCOUNT, STOCK_STATUS FROM ORDER_INFO
                     WHERE USERID='{}' AND STOCK_NAME='{}' AND STATUS=0;
                        """ #根据股票名查询交割单
SELECT_ORDER_INFO_ALL_SQL = """
                    SELECT ID, STOCK_NAME, CODE, TRADE_DATE, PRICE, VOLUME, ACCOUNT, STOCK_STATUS FROM ORDER_INFO
                     WHERE USERID='{}' AND STATUS=0;
                        """ #根据股票名查询交割单

DELETE_ORDER_INFO_SQL = """
                    UPDATE ORDER_INFO SET STATUS=1 WHERE ID={} AND USERID='{}';
                  """ #删除指定id的交割单

# ---------------------- mongodb ------------------
MONGODB_PORT = os.getenv("MONGODB_PORT", 28018)
MONGODB_IP = os.getenv("MONGODB_IP",'60.204.132.107')
MONGODB_NAME = os.getenv("MONGODB_NAME", 'smart_stock')
REALTIME_COLLECTION_NAME = 'real_time_table'
BACKTRADE_RECODE_COLLECTION_NAME = 'backtrader_record_table'
MONGODB_USER = os.getenv('MONGODB_USER', 'smart_stock')
MONGODB_PWD = os.getenv('MONGODB_PWD', 'smart_stock')