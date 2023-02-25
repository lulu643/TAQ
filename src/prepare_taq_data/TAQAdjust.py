import pandas as pd
from collections import defaultdict

from taq.src import MyDirectories
from taq.src.FileManager import FileManager


class TAQAdjust:
    def __init__(self):
        self.baseDir = MyDirectories.getTAQDir()
        self.adjFactorPath = self.baseDir + '/s&p500.xlsx'

    def read_adjust_factors(self, adj_type):
        """
        Read the adjustment factors from s&p500.xlsx
        """
        if adj_type == 'price':
            cols = 'B, H, BA'
        elif adj_type == 'vol':
            cols = 'B, H, BB'
        else:
            raise ValueError

        df = pd.read_excel(self.adjFactorPath, sheet_name='WRDS', usecols=cols)
        df = df.dropna(subset=['Names Date'])
        table = pd.pivot_table(df, index='Names Date', columns='Ticker Symbol')
        table.columns = table.columns.droplevel()
        table.index = pd.to_datetime(table.index.astype(int), format='%Y%m%d')
        return table

    def adjust_value(self, adjust_factor, trade_date, ticker, value):
        contem_factor = adjust_factor._get_value(trade_date, ticker)
        last_factor = adjust_factor[ticker].iloc[-1]
        return value / contem_factor * last_factor

    def adjust_prices(self, startDateString="20070919", endDateString="20070921"):
        # TODO: not sure the function works because the samples don't have adjustment
        original_price = defaultdict(list)
        adjusted_price = defaultdict(list)

        adjust_factor = self.read_adjust_factors('price')

        fm = FileManager(self.baseDir)
        tradeDates = fm.getTradeDates(startDateString, endDateString)
        tradeDates.sort()

        for i in range(len(tradeDates)):
            tradeTickers = fm.getTradeTickers(tradeDates[i])
            for ticker in tradeTickers:
                trade_file = fm.getTradesFile(tradeDates[i], ticker)
                # add to original price dictionary
                price = trade_file.getPrice(0)  # TODO: not sure about the argument here
                original_price[ticker].append(price)
                # add to adjusted price dictionary
                adj_price = self.adjust_value(adjust_factor, tradeDates[i], ticker, price)
                adjusted_price[ticker].append(adj_price)

        original_price_df = pd.DataFrame(original_price)
        original_price_df.to_csv("../../output/original_trades.csv", index=False)


if __name__ == "__main__":
    taq_adjust = TAQAdjust()
    taq_adjust.adjust_prices()