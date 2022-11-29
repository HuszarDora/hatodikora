import pandas as pd
import numpy as np
import scipy as sp
from matplotlib import pyplot as plt


class PortfolioOptimizer:
    def __init__(self, asset_price_file_loc, rf = 0.01):
        self._asset_file_loc = asset_price_file_loc
        self._read_asset_file()
        self._calc_asset_metrics()
        self._rf = rf
        self._asset_names = self._price_hist_df.columns
        self._n_asset = len(self._asset_names)

    def add_constraints(self,long_only = False,
                        fully_invested = True,
                        max_concentration = None):

        self._constraint_long_only =  long_only
        self._constraint_fully_invested =  fully_invested
        self._constraint_max_concentration =  max_concentration


    def _read_asset_file(self):
        price_hist_df = pd.read_csv(self._asset_file_loc, index_col=0)
        # one-liner list comp
        price_hist_df.columns = [colname.replace("_price", "") for colname in price_hist_df.columns]
        price_hist_df.index = pd.to_datetime(price_hist_df.index)
        # price_hist_df.columns = ['BLK', 'KO', 'GE', 'ATVI', 'JPM']

        price_hist_df.fillna(method="ffill")
        self._price_hist_df = price_hist_df

    def _calc_asset_metrics(self):
        self._return_asset = self._price_hist_df / self._price_hist_df.shift(1) - 1
        self._mean_asset = self._return_asset.mean() * 12
        self._std_asset = self._return_asset.std() * np.sqrt(12)
        self._cov_asset = self._return_asset.cov() * 12
        self._corr_asset = self._return_asset.corr()

    @staticmethod
    def _calc_nasset_mean(w, mean_return):
        return np.sum(w * mean_return)

    @staticmethod
    def _calc_nasset_std(w, cov_matrix):
        return np.sqrt(np.dot(np.dot(w, cov_matrix), w.transpose()))

    def calc_eff_frontier(self):
        eff_frontier = {}
        for return_target in np.linspace(0.01, 0.3, 100):
            cons = ({'type': 'eq', 'fun': lambda weight: return_target - self._calc_nasset_mean(weight, self._mean_asset)},
                    {'type': 'eq', 'fun': lambda weight: np.sum(weight) - 1})

            bounds = []
            # No short position - all the weights are positive
            # for i in range(mean_asset.shape[0]):
            #    bounds.append((0, 0.8))

            # if self._constraint_long_only:
            #     cons.append(...)

            res = sp.optimize.minimize(self._calc_nasset_std,
                                       np.array([1, 0, 0, 0, 0]),
                                       args=(self._cov_asset),
                                       constraints=cons)
            if res.success:
                eff_frontier[return_target] = res.x

        eff_frontier_df = pd.DataFrame(eff_frontier, index=self._asset_names).transpose()
        eff_frontier_df["Standard dev."] = eff_frontier_df.apply(lambda x: self._calc_nasset_std(np.array(x), self._cov_asset),
                                                                 axis=1)
        eff_frontier_df.reset_index(inplace=True)
        #eff_frontier_df.plot(x="Standard dev.", y="index")
        return eff_frontier_df

    def calc_CAL(self):
        cs, cs_deriv = self._calc_spline_for_eff_frontier()

        def system_of_equations(params):
            equation_1 = params[0] - self._rf
            equation_2 = params[1] - cs_deriv(params[2])
            equation_3 = params[0] + params[1] * params[2] - cs(params[2])
            return [equation_1, equation_2, equation_3]

        CAL_params = sp.optimize.fsolve(func=system_of_equations, x0 = [self._rf,0.2, 0.2])
        return CAL_params

    def _calc_spline_for_eff_frontier(self):
        eff_fr_points = self.calc_eff_frontier()
        index_to_filter = eff_fr_points["Standard dev."].argmin()
        eff_fr_points = eff_fr_points.loc[24:]
        cs = sp.interpolate.CubicSpline(eff_fr_points["Standard dev."], eff_fr_points["index"])
        cs_deriv = cs.derivative()
        return cs, cs_deriv

    def plot_eff_frontier_with_cal(self):
        eff_frontiert = self.calc_eff_frontier()
        cal_params = self.calc_CAL()
        eff_frontiert["CAL"] = cal_params[0] + eff_frontiert["Standard dev."]* cal_params[1]
        eff_frontiert.plot(x="Standard dev.", y=["CAL", "index"])
        plt.show()

    def plot_magic_carpet(self):
        eff_frontiert = self.calc_eff_frontier()
        eff_frontiert.plot(kind="bar", stacked =True, x="index", y=self._asset_names)
        plt.show()

if __name__ == "__main__":
    PO = PortfolioOptimizer("Price_history.csv")
    PO.add_constraints(long_only=True)
    PO.plot_eff_frontier_with_cal()
    PO.plot_magic_carpet()
