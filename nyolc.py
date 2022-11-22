import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from Option import Option

filename = 'KO.csv'
df = pd.read_csv(filename)
df.describe()
# print(df[:6])

df["date"] = pd.to_datetime(df["date"])
df["expiry"] = pd.to_datetime(df["expiry"])
df["daysToExp"] = (df.expiry-df.date).dt.days
df = df.set_index("date")
print(df[:6])

# plot forward price vs time
df.groupby(df.index).forward_price.median().plot()
plt.show()

def calcVolaMid(row):
    opt = Option(row.cp_flag, row.strike, row.expiry, 1)
    if row.forward_price*row.daysToExp*row.mid>0:
        return opt.calcVola(row.forward_price,row.daysToExp/365,row.mid)
    else:
        return np.nan

df0=df[df.index<"2018-03-01"]
df0.loc[:,"implied_vola_mid"]=df0.apply(calcVolaMid,axis=1)
print(df0)

# symbol="KO 180323C48000"
# df=df0[df0.symbol==symbol]

dates=df0.index.unique()

df_=df0[df0.index==dates[23]]
df_=df0[df0.daysToExp==102]
date=df_.index[0]
df_=df_[df_.last_date==date]
df_.groupby(df_.strike).implied_vola_mid.median().plot()
plt.show()



# def calcVolaBid(row):
#     opt = Option(row.cp_flag, row.strike, row.expiry, 1)
#     if row