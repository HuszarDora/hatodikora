import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def get_risk_free_rate():
    df=pd.read_csv('DTB3.csv')
    df.index=pd.to_datetime(df['DATE'])
    df=df[['DTB3']]
    df.columns=['risk_free']
    msk=df['risk_free']!='.'
    df=df[msk]
    df=df.astype(float)
    df=df/252
    return df
df=get_risk_free_rate()
print(df)


filename='BRK-B.csv'
df=pd.read_csv(filename)
df['ret_log']=np.log(df['Adj Close']/df['Adj Close'].shift(1))
df.index=pd.to_datetime(df['Date'])
df_risk_free=get_risk_free_rate()
df_joined=df.join(df_risk_free)
df['ret_log_daily_exc']=


t_day_in_year=252
vol_window_in_y=[0.25, 1, 3, 10]
mean_window_in_y=[0.25, 1, 3, 10]
cols_vol, cols_ret, cols_beta=[], [], []
for year in vol_window_in_y:
    col_vol='vol_rolling_'+str(year)+'y'
    cols_vol.append(col_vol)
    df[col_vol]=np.sqrt(252)*df['ret_log'].rolling(int(year*t_day_in_year)).std()

for year in mean_window_in_y:
    col_ret='mean_rolling_'+str(year)+'y'
    cols_ret.append(col_ret)
    df[col_ret]=t_day_in_year*df['ret_log'].rolling(int(year*t_day_in_year)).mean()

df['ret_log'].plot()
df[cols_vol].plot()
df[cols_ret].plot()
df[['ret_log','vol_rolling_1y','mean_rolling_1y']].plot()
plt.show()
print(1)
df['vol_rolling_1y']=df['ret_log'].rolling(252).std()
df['vol_rolling_2y']=df['ret_log'].rolling(504).std()

df[['vol_rolling_1y','vol_rolling_2y']].plot()
plt.show()
print(1)