import os 
import random
import hashlib
from src.utils.date_utils import *
from src.utils.network_utils import *
from src.utils.common import *

def _md5_obj():
    """根据python版本返回md5实例"""
    md5_obj = hashlib.md5()
    return md5_obj


def md5_from_binary(binary):
    """对字符串进行md5, 返回md5后32位字符串对象"""
    m = _md5_obj()
    m.update(binary.encode('utf-8'))
    return m.hexdigest()

def _create_random_tmp(salt_count, seed):
    """
    从seed种子字符池中随机抽取salt_count个字符，返回生成字符串,
    注意抽取属于有放回抽取方法
    :param salt_count: 生成的字符序列的长度
    :param seed: 字符串对象，做为生成序列的种子字符池
    :return: 返回生成字符串
    """
    # TODO random.choice有放回抽取方法, 添加参数支持无放回抽取模式
    sa = [random.choice(seed) for _ in range(salt_count)]
    salt = ''.join(sa)
    return salt

def create_random_with_num_low(salt_count):
    """
    种子字符池 = "abcdefghijklmnopqrstuvwxyz0123456789",
    从种子字符池中随机抽取salt_count个字符, 返回生成字符串,
    :param salt_count: 生成的字符序列的长度
    :return: 返回生成字符串
    """
    seed = "abcdefghijklmnopqrstuvwxyz0123456789"
    return _create_random_tmp(salt_count, seed)

def create_random_with_num(salt_count):
    """
    种子字符池 = "0123456789", 从种子字符池中随机抽取salt_count个字符, 返回生成字符串,
    :param salt_count: 生成的字符序列的长度
    :return: 返回生成字符串
    """
    seed = "0123456789"
    return _create_random_tmp(salt_count, seed)

def random_from_list(array):
    """从参数array中随机取一个元素"""
    # 在array长度短的情况下，测试比np.random.choice效率要高
    return array[random.randrange(0, len(array))]


K_DEV_MODE_LIST = ["A0001", "OPPOR9", "OPPOR9", "VIVOX5",
                    "VIVOX6", "VIVOX6PLUS", "VIVOX9", "VIVOX9PLUS"]
# 预先设置模拟手机请求的os version
K_OS_VERSION_LIST = ["4.3", "4.2.2", "4.4.2", "5.1.1"]
# 预先设置模拟手机请求的屏幕大小
K_PHONE_SCREEN = [[1080, 1920]]
g_market_trade_year = 250

class DataParseWrap(object):
    """
        做为类装饰器封装替换解析数据统一操作，装饰替换init
    """

    def __call__(self, cls):
        """只做为数据源解析类的装饰器，统一封装通用的数据解析规范及流程"""
        if isinstance(cls, six.class_types):
            # 只做为类装饰器使用
            init = cls.__init__

            def wrapped(*args, **kwargs):
                try:
                    # 拿出被装饰的self对象
                    warp_self = args[0]
                    warp_self.df = None
                    # 调用原始init
                    init(*args, **kwargs)
                    symbol = args[1]
                    # 开始数据解析
                    self._gen_warp_df(warp_self, symbol)
                except Exception as e:
                    logging.exception(e)

            # 使用wrapped替换原始init
            cls.__init__ = wrapped

            wrapped.__name__ = '__init__'
            # 将原始的init赋予deprecated_original，必须要使用这个属性名字，在其它地方，如AbuParamBase会寻找原始方法找它
            wrapped.deprecated_original = init
            return cls
        else:
            raise TypeError('DataParseWrap just for class warp')
        # noinspection PyMethodMayBeStatic
    def _gen_warp_df(self, warp_self, symbol):
        """
        封装通用的数据解析规范及流程
        :param warp_self: 被封装类init中使用的self对象
        :param symbol: 请求的symbol str对象
        :return:
        """

        # 规范原始init函数中必须为类添加了如下属性
        must_col = ['open', 'close', 'high', 'low', 'volume', 'date']
        # 检测所有的属性都有
        all_has = all([hasattr(warp_self, col) for col in must_col])
        # raise RuntimeError('df.columns must have |date|open|close|high|volume| ')
        if all_has:
            # 将时间序列转换为pd时间
            dates_pd = pd.to_datetime(warp_self.date)
            # 构建df，index使用dates_pd
            warp_self.df = pd.DataFrame(index=dates_pd)
            for col in must_col:
                # 所以必须有的类属性序列设置给df的列
                warp_self.df[col] = getattr(warp_self, col)

            # 从收盘价格序列shift出昨收价格序列
            warp_self.df['pre_close'] = warp_self.df['close'].shift(1)
            warp_self.df['pre_close'].fillna(warp_self.df['open'], axis=0, inplace=True)
            # 添加日期int列
            warp_self.df['date'] = warp_self.df['date'].apply(lambda x: date_str_to_int(str(x)))
            # 添加周几列date_week，值为0-4，分别代表周一到周五
            warp_self.df['date_week'] = warp_self.df['date'].apply(
                lambda x: week_of_date(str(x), '%Y%m%d'))

            # 类型转换
            warp_self.df['close'] = warp_self.df['close'].astype(float)
            warp_self.df['high'] = warp_self.df['high'].astype(float)
            warp_self.df['low'] = warp_self.df['low'].astype(float)
            warp_self.df['open'] = warp_self.df['open'].astype(float)
            warp_self.df['volume'] = warp_self.df['volume'].astype(float)
            warp_self.df['volume'] = warp_self.df['volume'].astype(np.int64)
            warp_self.df['date'] = warp_self.df['date'].astype(int)
            warp_self.df['pre_close'] = warp_self.df['pre_close'].astype(float)
            # 不使用df['close'].pct_change计算
            # noinspection PyTypeChecker
            warp_self.df['p_change'] = np.where(warp_self.df['pre_close'] == 0, 0,
                                                (warp_self.df['close'] - warp_self.df['pre_close']) / warp_self.df[
                                                    'pre_close'] * 100)

            warp_self.df['p_change'] = warp_self.df['p_change'].apply(lambda x: round(x, 3))
            # 给df加上name
            warp_self.df.name = symbol
            
@DataParseWrap()
class TXParser(object):
    """tx数据源解析类，被类装饰器AbuDataParseWrap装饰"""

    def __init__(self, symbol, json_dict):
        """
        :param symbol: 请求的symbol str对象
        :param sub_market: 子市场（交易所）类型
        :param json_dict: 请求返回的json数据
        """
        if json_dict['code'] == 0:
            data = json_dict['data'][symbol]

            if 'qfqday' in data.keys():
                data = data['qfqday']
            else:
                data = data['day']

            # 为AbuDataParseWrap准备类必须的属性序列
            if len(data) > 0:
                # 时间日期序列，时间格式为2017-07-26格式字符串
                self.date = [item[0] for item in data]
                # 开盘价格序列
                self.open = [item[1] for item in data]
                # 收盘价格序列
                self.close = [item[2] for item in data]
                # 最高价格序列
                self.high = [item[3] for item in data]
                # 最低价格序列
                self.low = [item[4] for item in data]
                # 成交量序列
                self.volume = [item[5] for item in data]

class TXApi:
    """tx数据源，支持港股，美股，a股"""

    K_NET_BASE = "http://ifzq.gtimg.cn/appstock/app/%sfqkline/get?p=1&param=%s,day,,,%d," \
                 "qfq&_appName=android&_dev=%s&_devId=%s&_mid=%s&_md5mid=%s&_appver=4.2.2&_ifChId=303&_screenW=%d" \
                 "&_screenH=%d&_osVer=%s&_uin=10000&_wxuin=20000&__random_suffix=%d"

    K_NET_HK_MNY = 'http://proxy.finance.qq.com/ifzqgtimg/stock/corp/hkmoney/sumary?' \
                   'symbol=%s&type=sum&jianjie=1&_appName=android' \
                   '&_dev=%s&_devId=%s&_mid=%s&_md5mid=%s&_appver=5.5.0&_ifChId=277' \
                   '&_screenW=%d&_screenH=%d&_osVer=%s&_uin=10000&_wxuin=20000&_net=WIFI&__random_suffix=%d'

    K_DB_TABLE_NAME = "values_table"
    K_DB_TABLE_SN = "stockCode"
    p_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.path.pardir))
    K_SYMBOLS_DB = os.path.join(p_dir, 'RomDataBu/symbols_db.db')

    def kline(self, symbol, n_folds=2, start=None, end=None):
        """日k线接口"""
        symbol = code_to_abu_code(symbol)
        cuid = create_random_with_num_low(40)
        cuid_md5 = md5_from_binary(cuid)
        random_suffix = create_random_with_num(5)
        dev_mod = random_from_list(K_DEV_MODE_LIST)
        os_ver = random_from_list(K_OS_VERSION_LIST)
        screen = random_from_list(K_PHONE_SCREEN)
        days = g_market_trade_year * n_folds + 1
        # start 不为空时计算 获取天数，获取的数据肯定比预期的数据多，因为同一时间内，交易日的天数一定不比实际的天数多
        if start:
            temp_end = current_str_date()
            days = diff(start, temp_end, check_order=False)
        
        market = ''
        url = TXApi.K_NET_BASE % (
            market, symbol, days,
            dev_mod, cuid, cuid, cuid_md5, screen[0], screen[1], os_ver, int(random_suffix, 10))
        data = get(url, timeout=200)
        if data is not None:
            kl_pd = TXParser(symbol, data.json()).df
        else:
            return None
        return self._fix_kline_pd_se(kl_pd, n_folds=n_folds, start=start, end=end)
    
    def _fix_kline_pd_se(self, kl_df, n_folds, start=None, end=None):
        """
        删除多余请求数据，即重新根据start，end或n_folds参数进行金融时间序列切割
        :param kl_df: 金融时间序列切割pd.DataFrame对象
        :param n_folds: n_folds年的数据
        :return: 删除多余数据，规则后的pd.DataFrame对象
        """
        if kl_df is None:
            return kl_df

        # 从start和end中切片
        if start is not None:
            # 有start转换为int，使用kl_df中的date列进行筛选切割
            start = date_str_to_int(start)
            kl_df = kl_df[kl_df.date >= start]
            if end is not None:
                # 有end转换为int，使用kl_df中的date列进行筛选切割
                end = date_str_to_int(end)
                kl_df = kl_df[kl_df.date <= end]
        else:
            # 根据n_folds构造切片的start
            start = begin_date(365 * n_folds)
            start = date_str_to_int(start)
            # 使用kl_df中的date列进行筛选切割
            kl_df = kl_df[kl_df.date >= start]
        return kl_df


if __name__ == '__main__':
    df = TXApi().kline('600640', start='2019-02-03')
