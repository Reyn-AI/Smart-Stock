import pandas as pd
import numpy as np
from datetime import datetime

def gen_predict_data(s_date, days, unique_id=1, freq='D', his_key=['vol', 'high', 'amount', 'open', 'low']):
    """生成预测数据"""
    data = np.array([unique_id]*days)
    df = pd.DataFrame(data, columns=['unique_id'])
    date = pd.date_range(start=s_date, periods=days, freq=freq)
    df['ds'] = date.to_pydatetime()
    df['y'] = 0    
    df[his_key] = 0
    return df
    

if __name__ == '__main__':
    df = gen_predict_data(s_date='2024-04-07', days=10)
    print(df)
    