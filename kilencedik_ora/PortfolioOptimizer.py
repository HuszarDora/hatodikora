import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy as sp

class PortfolioOptimizer:
    def __init__(self,asset_price_file_loc, rf=0.1):
        self._asset_file_loc=asset_price_file_loc
        self._read_asset_file()
        self._calc_asset_metrics()
        self._rf = rf

    def add_constraints(self, long_only = False, fully_invested=True, max_concentration=None):
        self.add_constraints_long_only = long_only
        self.add_constraints_fully_inveted = fully_invested
        self.add_constraints_max_concentration = max_concentration

    def _read_asset_file(self):
        price_hist_df = pd.read_csv(self._asset_file_loc, index_col=0)
        price_hist_df.columns = [colname.replace("_price", "") for colname in price_hist_df]
        price_hist_df.index = pd.to_datetime(price_hist_df.index)

        price_hist_df.fillna(method="ffill")
        self._price_hist_df = price_hist_df

    def _calc_asset_metrics(self):
        self._return_asset = self._price_hist_df / self._price_hist_df.shift(1) - 1
        self._mean_asset = self._return_asset.mean() * 12
        self._std_asset = self._return_asset.std() * np.sqrt(12)
        self._cov_asset = self._return_asset.cov() * 12
        self._corr_asset = self._return_asset.corr()


    @staticmethod
    def _calc_nasset_mean(w,mean_return):
        return np.sum(w * mean_return)

    @staticmethod
    def _calc_nasset_std(w, cov_matrix):
        return np.sqrt(np.dot(np.dot(w, cov_matrix), w.transpose()))

    def calc_eff_frontier(self):
        eff_frontier = {}
        for return_target in np.linspace(0.01, 0.3, 100):
            # return_target = 0.2
            cons = ({'type': 'eq', 'fun': lambda weight: return_target - self._calc_nasset_mean(weight, self._mean_asset)},
                    {'type': 'eq', 'fun': lambda weight: np.sum(weight) - 1})
            # {'type': 'ineq', 'fun':lambda weight:np.max(weight)-0.8} #fully invested
            res = sp.optimize.minimize(self._calc_nasset_std, np.array([1, 0, 0, 0, 0]), args=(self._cov_asset),
                                       constraints=cons)  # ,bounds=bounds)
            if res.success:
                eff_frontier[return_target] = res.x
        # bounds=[]
        # No short position - all the weight are pozitive
        # for i in range(mean_asset.shape[0]):
        #     bounds.append((0, None)) #ha szeretnénk felső korlátot a None-t lehet átírni pl 0.8-ra

        # 91%-ban fektet az egyikbe, 85%-ban egy másikba a többibe közel 0%-ban

        eff_frontier_df = pd.DataFrame(eff_frontier).transpose()
        eff_frontier_df["Standard dev."] = eff_frontier_df.apply(lambda x: self._calc_nasset_std(np.array(x), self._cov_asset),
                                                                 axis=1)
        eff_frontier_df.reset_index(inplace=True)
        # eff_frontier_df.plot(x="Standard dev.", y="index")
        # plt.show()
        return eff_frontier_df

    def calc_CAL(self):
        cs, cs_deriv = self._calc_spine_for_eff_frontier()

        def system_of_equations(params):
            equation_1 = params[0] - self._rf
            equation_2 = params[1] - cs_deriv(params[2])
            equation_3 = params[0] + params[1] * params[2] - cs(params[2])
            return [equation_1, equation_2, equation_3]

        CAL_params = sp.optimize.fsolve(func=system_of_equations, x0 = [self._rf, 0.2, 0.2])

    def _calc_spine_for_eff_frontier(self):
        eff_fr_points = self.calc_eff_frontier()
        index_to_filter = eff_fr_points["Standard dev."].argmin()
        eff_fr_points = eff_fr_points.loc[24:]
        cs = sp.interpolate.CubicSpline(eff_fr_points["Standard dev."], eff_fr_points["index"])
        cs_deriv = cs.derivative()
        return cs, cs_deriv

if __name__=="__main__":
    PO = PortfolioOptimizer("Price_history.csv")
    PO.add_constraints(long_only=True)
    # eff_frontier = PO.calc_eff_frontier()
    CAL = PO.calc_CAL()
    pass
