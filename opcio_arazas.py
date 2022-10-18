import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

from Option import Option

opt=Option("C",100,"20221215",1)

# print(opt.calcPrice(110,0.5,0.3,0))
# print(opt.calcPayoff(139))

K=360
expiry="20221215"
C=Option("C",K,expiry,1)
P=Option("P",K,expiry,-1)

S=3455
t=0.23
vola=0.3

# put-call paritas: C(t)-P(t)=S(t)-K --> a P-ben lévő -1 miatt kell a + jel a C és P közé
print(C.calcPrice(S,t,vola) + P.calcPrice(S,t,vola) - S + K)

spots=range(250,500,5)
prices=[C.calcPrice(s,1,vola) for s in spots]
pays=[C.calcPayoff(s) for s in spots]

plt.plot(spots,pays,spots,prices)
plt.show()

# ha a vola=0 akkor =payoff