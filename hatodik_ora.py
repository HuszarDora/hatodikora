import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df=pd.DataFrame(columns=['n','fib'])

#append,pd.concat, pd.merge, pd.join
row1={'n':1,'fib':1}
row2={'n':2,'fib':1}
new_df=pd.DataFrame([row1,row2])
df=pd.concat([df,new_df],axis=0,ignore_index=True)
# ugyan az mint az mint a előző:
# df=df.append({'n':1,'fib':1},ignore_index=True)
# print(df)

# how to iterate over dataframe
df2=pd.DataFrame(range(1,21),columns=['n'])
df2['fib']=np.nan
# df2.loc[df2['n']==1,'fib']=1
# df2.loc[df2['n']==2,'fib']=1
# df2.loc[df2['n'] in [1,2],'fib']=1



for ix, row in df2.iterrows():
    # if ix in [1,2]:
    n=row['n']
    if n in [1,2]:
    # if ix in [0, 1]:
        # row['fib']=1
        df2.loc[ix,'fib'] = 1
    else:
        df2.loc[ix,'fib']=df2.loc[ix-1,'fib']+df2.loc[ix-2,'fib']
    # print(ix)
    # print(row)
    # print(row['n'])
# print(df2)

class VelSzamok():
    def __init__(self,n_rows,n_cols):
        self.n_rows=n_rows
        self.n_cols=n_cols
        self.value=np.random.random((self.n_rows,self.n_cols))
        pass
    def plot_column_averages(self,show=True):
        averages=self.value.mean(axis=0)
        print(averages)
        plt.plot(averages)
        if show:
            plt.show()
        pass

a=VelSzamok(6000,3)
print(a.value)
a.plot_column_averages()
