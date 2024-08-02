from src.utils.registy import factor_calculate_register
import backtrader as bt
from src.backtest.strategys.factors.base_factor import BaseFactorCalculate
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from array import array
np.random.seed(0) #保证随机数生成的一致性
import pandas as pd
    
@factor_calculate_register(name='RSRS', must_params=['high', 'low'], desc='右偏标准分承压分析', view='subChart')
class RSRS(BaseFactorCalculate):
    
    def call_metric(self, *args, **kwargs):
        """计算斜率"""
        if 'high' in kwargs.keys() and 'low' in kwargs.keys():
            high_array = np.array(kwargs.get('high', []))
            low_array = np.array(kwargs.get('low', []))
        else:
            assert len(args)>1
            high_array = np.array(args[0])
            low_array = np.array(args[1])
        N = int(kwargs.get('N', 16))
        M = int(kwargs.get('M', 300))
        min_M = int(kwargs.get('min_M', 20))
        betas = np.array([np.nan]*len(high_array))
        R2s = np.array([np.nan]*len(high_array))
        std_scores = np.array([np.nan]*len(high_array)) #标准分
        mdf_std_scores = np.array([np.nan]*len(high_array)) #优化标准分
        rsk_std_score = np.array([np.nan]*len(high_array)) #右偏标准分
        for i in range(len(high_array)):
            if i <N-1:
                betas[i] = 0
                R2s[i] = 0
            else:
                x = np.array(high_array[i+1-N:i+1])
                y = np.array(low_array[i+1-N:i+1])
                lr = LinearRegression().fit(x.reshape(-1,1), y)
                y_pred = lr.predict(x.reshape(-1, 1))
                beta = lr.coef_[0]
                r2 = r2_score(y, y_pred)
                betas[i] = beta
                R2s[i] = r2
                if i+1 >= M:
                    std_scores[i] = (beta - np.mean(betas[i+1-M:i+1]))/ np.std(betas[i+1-M: i+1])
                elif i+1>=min_M and i+1<M:
                    std_scores[i] = (beta - np.mean(betas[i+1-min_M:i+1]))/ np.std(betas[i+1-min_M:i+1])
                mdf_std_scores[i] = r2 * std_scores[i]
                rsk_std_score[i] = betas[i] * mdf_std_scores[i]
        if kwargs.get('src') is not None:
            return rsk_std_score, kwargs.get('src') #多进程时跟df对应
        return rsk_std_score   
    
    def __call__(self, *args, **kwargs):
        return self.call_metric(*args, **kwargs)

