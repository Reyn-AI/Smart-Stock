from src.backtest.strategys.factors.eval.alpha_engine import AlphaLenEngine
import alphalens
from src.utils.stock_utils import *
from src.backtest.strategys.factors import RSRS
def test_rsrs():
    engine = AlphaLenEngine()
    # codes = get_codes_by_zs_code('sz50')
    df_list = get_day_k_data_multi(codes=['600640', '600641'], n_folds=1, return_list=True)
    df_rsrs_list = []
    for df in df_list:
        df['rsrs'] = RSRS().call_metric(high=df.high, low=df.low)
        df_rsrs_list.append(df)
    res = pd.concat(df_rsrs_list, axis=0)
    res = engine.forward_returns(df=res, factor_name='rsrs')
    # alphalens.tears.create_full_tear_sheet(res)
    breakpoint()

test_rsrs()