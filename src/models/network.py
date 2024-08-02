
from typing import List, Dict
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from neuralforecast import NeuralForecast
from src.models.dataloader import JsonDataLoader
import os
from src.models.utils import *
from src.utils.common import get_default_output_path


# todo 涨跌幅限制约束 引入星期变量
class TrainModel:
    
    def __init__(self, codes:List=[], json_path:str=None, s_date="2019-01-01", e_date='2025-01-01'):
        self.codes = codes
        self.json_path = json_path
        self.s_date = s_date
        self.e_date = e_date
        self.save_dir = get_default_output_path()
        
    def load_data(self):
        if self.json_path and os.path.exists(self.json_path):
            df = JsonDataLoader(json_path=self.json_path).load()
        elif len(self.codes) > 0 :
            df = JsonDataLoader().load_from_web(codes=self.codes, s_date=self.s_date, e_date=self.e_date)
        df['week_day'] = df['ds'].apply(lambda x: x.weekday())
        df = self.time_contiguous(df)
        return df 
    
    def train(self, models: List, train_df=None, *args, **kwargs):
        freq = kwargs.get('freq', 'D')
        nf = NeuralForecast(models=models, freq=freq)
        if train_df is None:
            train_df = self.load_data()
        nf.fit(df=train_df)
        nf.save(path=f'{self.save_dir}/checkpoints/test_run/',
            model_index=None, 
            overwrite=True,
            save_dataset=True)
        return nf
    
    def predict(self, nf: NeuralForecast, df=None, **kwargs):
        Y_hat_df = nf.predict(df, **kwargs).reset_index()
        save_path = os.path.join(self.save_dir, f'predict_txt/predict.csv')
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        Y_hat_df.to_csv(save_path, sep=',')
        print(save_path)
        return Y_hat_df
    
    def plot(self, code, y_train, model_names: List, pre_df, y_test=None):
        fig, ax = plt.subplots(1, 1, figsize = (20, 7))
        if y_test is not None:
            pre_df = y_test.merge(pre_df, how='outer', on=['unique_id', 'ds'])
        plot_df = pd.concat([y_train, pre_df]).set_index('ds')
        plot_df[['y']+model_names].plot(ax=ax, linewidth=2)
        ax.set_title('AirPassengers Forecast', fontsize=22)
        ax.set_ylabel('Monthly Passengers', fontsize=20)
        ax.set_xlabel('Timestamp [t]', fontsize=20)
        ax.legend(prop={'size': 15})
        ax.grid()
        save_dir = os.path.join(self.save_dir, f'predict_png/')
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, f'{code}.png')
        plt.savefig(save_path)
        print(save_path)
        
    def load_model(self, path):
        assert os.path.exists(path)
        nf = NeuralForecast.load(path='./checkpoints/test_run/')
        return nf

    def time_contiguous(self, df, freq='D'):
        """将时序变连续"""
        index_range = pd.date_range(start=df['ds'].min(), end=df['ds'].max(), freq=freq)
        filled_df = df.set_index('ds').reindex(index=index_range)
        filled_df = filled_df.fillna(method='ffill')
        filled_df = filled_df.reset_index()
        filled_df.rename(columns={'index':'ds'}, inplace=True)
        return filled_df


    
    
if __name__ == '__main__':
    from neuralforecast.models import *
    from neuralforecast.auto import AutoNBEATS, AutoNHITS
    from src.models.losses.loss import MixLoss
    from neuralforecast.auto import tune
    import utilsforecast.processing as ufp

    tool = TrainModel(codes=['003027'])
    df = tool.load_data()
    train_df = df[df.ds<='2024-3-18']
    test_df = df[df.ds>'2024-03-18']
    horizon = len(test_df)
    input_size = 2*horizon
    train_steps = 300
    models = [
            NBEATS(input_size=input_size, h=horizon, max_steps=train_steps, hist_exog_list=['open', 'high', 'low', 'pre_close', 'change', 'amount'], scaler_type='robust'),
        #   NBEATS(input_size=input_size, h=horizon, max_steps=train_steps, hist_exog_list=['open', 'high', 'low', 'vol', 'amount'], loss=MixLoss()),
        #   NBEATS(input_size=input_size, h=horizon, max_steps=train_steps, hist_exog_list=['open', 'high', 'low', 'vol', 'amount'], scaler_type='standard')
          TSMixerx(input_size=input_size, h=horizon, max_steps=train_steps,
                hist_exog_list=['open', 'high', 'low', 'pre_close', 'change'], futr_exog_list=['week_day'], scaler_type='robust', n_series=1),
        #   StemGNN(h=horizon, input_size=input_size, n_series=1)
        #   AutoNBEATS(h=horizon),
        #   PatchTST(input_size=input_size, h=horizon, max_steps=train_steps)
          ]
    # config_nhits = {
    #         "input_size": tune.choice([48, 48*2, 48*3]),              # Length of input window
    #         "start_padding_enabled": True,
    #         "n_blocks": 5*[1],                                              # Length of input window
    #         "mlp_units": 5 * [[64, 64]],                                  # Length of input window
    #         "n_pool_kernel_size": tune.choice([5*[1], 5*[2], 5*[4],         
    #                                         [8, 4, 2, 1, 1]]),            # MaxPooling Kernel size
    #         "n_freq_downsample": tune.choice([[8, 4, 2, 1, 1],
    #                                         [1, 1, 1, 1, 1]]),            # Interpolation expressivity ratios
    #         "learning_rate": tune.loguniform(1e-4, 1e-2),                   # Initial Learning rate
    #         "scaler_type": tune.choice([None]),                             # Scaler type
    #         "max_steps": tune.choice([1000]),                               # Max number of training iterations
    #         "batch_size": tune.choice([1, 4, 10]),                          # Number of series in batch
    #         "windows_batch_size": tune.choice([128, 256, 512]),             # Number of windows in batch
    #         "random_seed": tune.randint(1, 20),                             # Random seed
    #     }
    
    # models = [AutoNHITS(h=horizon, config=config_nhits)]
    nf = tool.train(models=models, train_df=train_df)
    fcsts_df = ufp.make_future_dataframe(
            uids=test_df.unique_id.drop_duplicates(),
            last_times=pd.DatetimeIndex([train_df.ds.max()]),
            freq='D',
            h=horizon,
            id_col='unique_id',
            time_col='ds',
        )
    # fcsts_df.ds = test_df.ds
    fcsts_df['week_day'] = fcsts_df['ds'].apply(lambda x:x.weekday())
    # fcsts_df = fcsts_df.sort_values(by=['ds'], ascending=[True])
    # fcsts_df = fcsts_df.reset_index(drop=True)
    pre_df = tool.predict(nf=nf, futr_df=fcsts_df)
    tool.plot(code='003027', y_train=train_df, pre_df=pre_df, y_test=test_df, model_names=['TSMixerx', 'NBEATS'])