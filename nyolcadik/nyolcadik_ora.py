import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

filename='BRK-B.csv'
df=pd.read_csv(filename)
df['ret_log']=np.log(df['Adj Close']/df['Adj Close'].shift(1))
df.index=pd.to_datetime(df['Date'])
t_day_in_year=252
vol_window_in_y=[1, 2, 5, 10]
cols=[]
for year in vol_window_in_y:
    col='vol_rolling_'+str(year)+'y'
    cols.append(col)
    df[col]=np.sqrt(252)*df['ret_log'].rolling(year*t_day_in_year).std()
df[cols].plot()
plt.show()
print(1)
df['vol_rolling_1y']=df['ret_log'].rolling(252).std()
df['vol_rolling_2y']=df['ret_log'].rolling(504).std()

df[['vol_rolling_1y','vol_rolling_2y']].plot()
plt.show()
print(1)