import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy as sp

# MPT Modern Portfolio Theory
# '52 részvények
# sure bet- biztos tipp
# diverzifikáció: ne egy helyre rakd a pénzed
# efficent frontier számolása lez a cél
# eloszlások között nincs kapcsolat. Nincs meghatározott eloszlásuk.
# hozam kockázati mérőszám, szórás, várható érték megbecslése: histórikus adatokból
# ri (i=1:n) wj (j=1:n) E(ri) Szig(ri)
# E(rP)=Szum(wj*E(ri)
# Var(rp)=w1^2*Var(r1)+w2^2*Var(r2)+2*w1*w2*Cov(r1,r2)=w^T*szum(w)
# Szoras(rp)=sqrt(Var(rp))






# Írjunk függvényt, ami kiszámolja a fontosabb eszközmetrikákat
# return
# várható return
# std

def eszkoz_metrikak(price_df):
    return_asset = price_df / price_df.shift(1) - 1
    mean_asset = return_asset.mean() * 12
    std_asset = return_asset.std() * np.sqrt(12)
    cov_asset = return_asset.cov() * 12
    corr_asset = return_asset.corr()
    return return_asset, mean_asset, std_asset, cov_asset, corr_asset



if __name__== "__main__":
    price_hist_df = pd.read_csv("Price_history.csv", index_col=0)
    # price_hist_df.columns = ['date','BLK','KO','GE','ATVI','JPM']
    price_hist_df.columns = [colname.replace("_price", "") for colname in price_hist_df]
    price_hist_df.index = pd.to_datetime(price_hist_df.index)
    price_hist_df.fillna(method="ffill")

    ret_asset, mean_asset, std_asset, cov_asset, corr_asset = eszkoz_metrikak(price_hist_df)

    ret_asset_ext = ret_asset.copy()
    ret_asset_ext["Pre-2015"] = ret_asset_ext.index.year < 2015

def calc_2asset_mean_std(w1,w2,ret1,ret2,sd1,sd2,corr):
    ptf_return = w1*ret1+w2*ret2
    ptf_std = w1**2*sd1**2+w2**2*sd2**2
    ptf_std = np.sqrt(ptf_std)
    return ptf_return, ptf_std

def calc_nasset_mean(w, mean_return):
    return np.sum(w*mean_return)

def calc_nasset_std(w, cov_matrix):
    return np.sqrt(np.dot(np.dot(w,cov_matrix),w.transpose()))

def calc_nasset_mean_std(w, mean_return, cov_matrix):
    ret = calc_nasset_mean(w, mean_return)
    std = calc_nasset_std(w, cov_matrix)
    return ret, std

w1s = np.linspace(-1, 1, 11)
twoassetptf_dict = {}
for w1 in w1s:
    ptf_ret, ptf_std = calc_2asset_mean_std(w1, 1-w1, mean_asset["BLK"], mean_asset["JPM"], std_asset["BLK"], std_asset["JPM"], corr_asset.loc["BLK","JPM"])
    twoassetptf_dict[w1] = (ptf_ret, ptf_std)

twoassetptf_df = pd.DataFrame(twoassetptf_dict).transpose()
twoassetptf_df.columns = ["Portfolio Return", "Portfolio Std. Dev."]
twoassetptf_df.plot(x="Portfolio Std. Dev.", y="Portfolio Return")
# plt.show()

# plt.scatter(ret_asset["BLK"], ret_asset["KO"])
# plt.suptitle("BKL és KO hozamok")
# plt.show()

sns.pairplot(ret_asset_ext,hue="Pre-2015")
# plt.show()

#3.feladat

calc_nasset_mean_std(np.array([1,0,0,0,0]), mean_asset, cov_asset)

grid = np.array(np.meshgrid(w1s,w1s,w1s,w1s))
grid = grid.reshape((4,-1)).transpose()
grid = np.c_[grid, 1-grid.sum(axis=1)]

nsasset_mean_std = []
for i in range(grid.shape[0]):
    ret,std = calc_nasset_mean_std(grid[i], mean_asset,cov_asset)
    nsasset_mean_std.append((ret,std))

nsasset_mean_std_df = pd.DataFrame(nsasset_mean_std)
nsasset_mean_std_df.columns = ["Portfolio Return", "Portfolio Std. Dev."]
nsasset_mean_std_df.plot.scatter(x="Portfolio Std. Dev.", y="Portfolio Return")
# plt.show()

# 4.feladat optimalizáció
eff_frontier = {}
for return_target in np.linspace(0.01, 0.3, 100):
    # return_target = 0.2
    cons = ({'type' : 'eq', 'fun': lambda weight: return_target - calc_nasset_mean(weight,mean_asset)},
            {'type' : 'eq', 'fun': lambda weight: np.sum(weight)-1})
            # {'type': 'ineq', 'fun':lambda weight:np.max(weight)-0.8} #fully invested
    res = sp.optimize.minimize(calc_nasset_std, np.array([1,0,0,0,0]), args=(cov_asset), constraints=cons) # ,bounds=bounds)
    if res.success:
        eff_frontier[return_target] = res.x
# bounds=[]
# No short position - all the weight are pozitive
# for i in range(mean_asset.shape[0]):
#     bounds.append((0, None)) #ha szeretnénk felső korlátot a None-t lehet átírni pl 0.8-ra


eredmeny = res.x
#91%-ban fektet az egyikbe, 85%-ban egy másikba a többibe közel 0%-ban


eff_frontier_df = pd.DataFrame(eff_frontier).transpose()
eff_frontier_df["Standard dev."] = eff_frontier_df.apply(lambda x: calc_nasset_std(np.array(x), cov_asset), axis=1)
eff_frontier_df.reset_index(inplace=True)
eff_frontier_df.plot(x="Standard dev.", y="index")
plt.show()
print(np.sum(res.x)) #1 az eredmény
pass