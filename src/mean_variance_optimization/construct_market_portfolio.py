import pandas as pd

from src import MyDirectories


class ConstructMarketPortfolio:
    def __init__(self):
        self.baseDir = MyDirectories.getTAQDir()
        self.ExcelPath = self.baseDir + '/s&p500.xlsx'

    def get_the_weights(self, date):
        """
        Compute the weights of each asseet in market portfolio on specific date
        using the formula:
        w_i = market capitalization of asset i / total market capitalization
        """
        df = pd.read_excel(self.ExcelPath, sheet_name='WRDS')
        # select the columns to use
        df = df [["Names Date",
                  "Ticker Symbol",
                  "Price or Bid/Ask Average",
                  "Shares Outstanding"]]
        # drop nan and none
        df = df.dropna(subset=df.columns)
        # select the date we are interested in
        df["Names Date"] = pd.to_datetime(df["Names Date"].astype(int), format='%Y%m%d')
        df = df[df['Names Date'] == pd.Timestamp(date)]
        # compute market cap of each asset
        df['market cap'] = df.apply(lambda x: x["Price or Bid/Ask Average"] * x["Shares Outstanding"], axis=1)
        # get the weight of an asset in the market portfolio
        sum_cap = df['market cap'].sum()
        df['weight'] = df['market cap'] / sum_cap
        # clean and organize the dataframe
        # Issue1: ['STZ', 'CBS', 'MKC', 'LEN', 'TAP'] have duplicate rows with diff prices and shares outstanding
        # deal with it by naming the duplicates as xxx, xxx_duplicate
        mask = df['Ticker Symbol'].duplicated(keep='first')
        df.loc[mask, 'Ticker Symbol'] = df.loc[mask, 'Ticker Symbol'] + '_duplicate'
        # set tickers as index
        df = df.set_index('Ticker Symbol')
        df.columns = ['Date', 'Price', 'SharesOutstanding', 'MarketCap', 'Weight']
        return df

    def compute_turnover(self, date1='2007-06-20', date2='2007-09-20'):
        # get the market cap weight of the assets in date1 and date2
        weights1 = self.get_the_weights(date1)['Weight']
        weights2 = self.get_the_weights(date2)['Weight']
        # concatenate the two weights series and fill na as 0 weight
        weights = pd.concat([weights1, weights2], axis=1)
        weights = weights.fillna(0)
        # Calculate the difference in weights between the two periods
        weight_diff = weights.diff(axis=1)
        # Drop the first column of weight_diff (which contains NaN values)
        weight_diff.dropna(axis=1, inplace=True)
        # Calculate the turnover ratio
        turnover_ratio = weight_diff.abs().sum().sum() / 2.0
        print("Portfolio Turnover Ratio: {:.2f}".format(turnover_ratio))
        return turnover_ratio


if __name__ == "__main__":
    obj = ConstructMarketPortfolio()
    obj.compute_turnover()
