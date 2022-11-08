import pandas as pd

from Option import Option

opt=Option("C",100,"20221215",1)

# print(opt.calcPrice(110,0.5,0.3,0))
# print(opt.calcPayoff(139))

K=380
expiry="20221215"
C=Option("C",K,expiry,1)
P=Option("P",K,expiry,-1)

vola=0.3
S=3455
t=0.23

# print(C.calcPrice(110,0.5,0.3,0))


# put-call paritas: C(t)-P(t)=S(t)-K --> a P-ben lévő -1 miatt kell a + jel a C és P közé
# print(C.calcPrice(S,t,vola) + P.calcPrice(S,t,vola) - S + K)

spots=range(250,500,5)
prices=[C.calcPrice(s,1,vola) for s in spots]
pays=[C.calcPayoff(s) for s in spots]

# plt.plot(spots,pays,spots,prices)
# plt.show()

# ha a vola=0 akkor =payoff


from Option import GBrown
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

gb = GBrown()
sigma = 0.35
N = 250
S0 = 100
spots = gb.generate(S0, 0, sigma, 1, N)
times = np.arange(0, 1, 1/N)
plt.plot(times, spots)
plt.show()

opt=Option("C",S0,None,1)

vola=0.35
prices=[]
deltas=[]
for (t,S) in zip(times, spots):
    price=opt.calcPrice(S,1-t,vola)
    delta=opt.calcDelta(S,1-t,vola)
    prices.append(price)
    deltas.append(delta)

plt.plot(times,np.array(prices))
plt.show()

df = pd.DataFrame({"time":times,"spot":spots})

K=100
def calcPrice(row):
    opt = Option("C",S0,None,1)
    vola = 0.3
    return opt.calcPrice(row.spot,1-row.time,vola)

df["price"]=df.apply(calcPrice,axis=1)