import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from neuralforecast import NeuralForecast
from neuralforecast.models import NBEATS, NHITS,PatchTST, Informer
from neuralforecast.losses.pytorch import QuantileLoss
from neuralforecast.utils import AirPassengersDF
from src.models.dataloader import JsonDataLoader
import os
import torch
from src.models.utils import *

# Split data and declare panel dataset
Y_df = JsonDataLoader().load_from_web(codes=['603912'], s_date='2022-01-01', e_date='2024-04-07')

# Y_df = AirPassengersDF
# Y_train_df = Y_df[Y_df.ds<='2024-03-10'] # 132 train
# Y_test_df = Y_df[Y_df.ds>'2024-03-10'] # 12 test
Y_train_df = Y_df

# Fit and predict with NBEATS and NHITS models
# horizon = len(Y_test_df)
# predict_df = gen_predict_data(s_date='2024-03-10', days=horizon, unique_id='000792')
horizon = 10
input_size = 3*horizon
train_steps = 300
models = [
          NBEATS(input_size=input_size, h=horizon, max_steps=train_steps, hist_exog_list=['open', 'high', 'low', 'vol', 'amount'], scaler_type='robust'),
          NHITS(input_size=input_size, h=horizon, max_steps=train_steps,
                hist_exog_list=['open', 'high', 'low', 'vol', 'amount'], scaler_type='robust'),

          ]
nf = NeuralForecast(models=models, freq='D')
nf.fit(df=Y_train_df)
# if torch.distributed.get_rank() == 0:
Y_hat_df = nf.predict().reset_index()
# if torch.distributed.get_rank() == 0:
#     breakpoint()
print(Y_hat_df)
# Plot predictions
fig, ax = plt.subplots(1, 1, figsize = (20, 7))
# Y_hat_df = Y_test_df.merge(Y_hat_df, how='left', on=['unique_id', 'ds'])
plot_df = pd.concat([Y_train_df, Y_hat_df]).set_index('ds')
plot_df[['y', 'NBEATS', 'NHITS']].plot(ax=ax, linewidth=2)

ax.set_title('AirPassengers Forecast', fontsize=22)
ax.set_ylabel('Monthly Passengers', fontsize=20)
ax.set_xlabel('Timestamp [t]', fontsize=20)
ax.legend(prop={'size': 15})
ax.grid()
plt.savefig('./test.png')


