from cvxopt import matrix
from cvxopt.blas import dot
from cvxopt.solvers import qp, options
import numpy as np
import pandas as pd

from math import sqrt


class ConstructMarketPortfolio:
    def __init__(self):
        self.ExcelPath = "/Users/sihanliu/Desktop/AlgoTradingCourse/taq/data/s&p500.xlsx"
        self.m = np.nan  # to store the estimation of mean
        self.c = np.nan  # to store the estimation of covariance matrix
        self.n = 0  # number of tickers I'm working on

    def get_returns(self):
        """
        From the S&P500 Excel file, extract daily return for all dates all assets
        """
        df = pd.read_excel(self.ExcelPath, sheet_name='WRDS')
        df = df[["Names Date", "Ticker Symbol", "Returns"]]
        df = df.dropna(subset=['Names Date'])
        # Most of the values in this column is of type "float", but some have value 0, 'B', or 'C'; drop 'B', 'C'
        df = df[df["Returns"].apply(lambda x: isinstance(x, (float, int)))]
        table = pd.pivot_table(df, index='Names Date', columns='Ticker Symbol', fill_value=np.nan)
        table.columns = table.columns.droplevel()
        table.index = pd.to_datetime(table.index.astype(int), format='%Y%m%d')
        return table

    def find_mean_covariance(self, ret_df, date):
        """
        Find the mean and covariance estimation of all assets for a given date
        date format example: '2007-06-20'
        """
        row = ret_df.loc[date]
        row = row.dropna()
        tickers = row.index.tolist()
        self.n = len(tickers)
        d = np.array(row).reshape(1, -1)
        self.m = np.mean(d, axis=0)
        self.c = np.cov(d.T)
        print(self.m)
        print(self.c)  # TODO: cannot get a valid covariance matrix because of data shape
        return self.m, self.c

    def mean_variance_optimization(self):
        n = self.n
        S = self.c
        pbar = self.m

        G = matrix(0.0, (n, n))  # TODO: whether to change this part depends on inequality constraint
        G[::n + 1] = -1.0
        h = matrix(0.0, (n, 1))
        A = matrix(1.0, (1, n))
        b = matrix(1.0)

        N = 100
        mus = [10 ** (5.0 * t / N - 1.0) for t in range(N)]
        options['show_progress'] = False
        xs = [qp(mu * S, -pbar, G, h, A, b)['x'] for mu in mus]
        returns = [dot(pbar, x) for x in xs]
        risks = [sqrt(dot(x, S * x)) for x in xs]

        try:
            import pylab
        except ImportError:
            pass
        else:
            pylab.figure(1, facecolor='w')
            pylab.plot(risks, returns)
            pylab.xlabel('standard deviation')
            pylab.ylabel('expected return')
            pylab.axis([0, 0.2, 0, 0.15])
            pylab.title('Risk-return trade-off curve')
            pylab.yticks([0.00, 0.05, 0.10, 0.15])
            pylab.title('Optimal allocations')
            pylab.show()


if __name__ == "__main__":
    obj = ConstructMarketPortfolio()
    returns = obj.get_returns()
    obj.find_mean_covariance(returns, '2007-09-20')
