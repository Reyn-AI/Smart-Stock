from nixtlats import NixtlaClient
import pandas as pd
from src.models.network import TrainModel

nixtla_client = NixtlaClient(api_key = 'nixt-kiA0XndVchhyhWOUYZqHG6PaUT4BnBpD8VHjcY5WMronzYYSphwDQcqT8eF9gbgfCH3V5XsFcQktt6Eo')

tool = TrainModel(codes=['003027'], e_date='2024-04-09')
df = tool.load_data()

# df1 = pd.read_csv('https://raw.githubusercontent.com/Nixtla/transfer-learning-time-series/main/datasets/electricity-short.csv')
fcst_df = nixtla_client.forecast(df, h=20, level=[80, 90], freq='D', add_history=False)
fcst_df.to_csv('./time_gpt.csv', sep=',')
fig = nixtla_client.plot(df, fcst_df, level=[80, 90], max_insample_length=24 * 5)
fig.savefig('./time_gpt.png')