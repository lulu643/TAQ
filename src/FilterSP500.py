import os
import pandas as pd
import MyDirectories


class FilterSP500:
    def __init__(self):
        self.baseDir = MyDirectories.getTAQDir()
        self.tradesDir = MyDirectories.getTradesDir()
        self.quotesDir = MyDirectories.getQuotesDir()

    def get_SP500_tickers(self):
        """
        Get all S&P500 tickers from the Excel given
        """
        # TODO: 不确定这个要不要根据每一天的时间来生成list
        file_path = self.baseDir + '/s&p500.xlsx'
        df = pd.read_excel(file_path, sheet_name='WRDS', usecols='H')
        tickers = set(df.iloc[:, 0].unique().flatten())
        # with open("utils/s&p500_list.txt", "w") as output:
        #     output.write(str(tickers))
        return tickers

    def filter_trades(self, tickers):
        """
        In trades folder, delete the files not in S&P500 list
        """
        removed = []
        for root, dirs, files in os.walk(self.tradesDir):
            for filename in files:
                if filename[:-13] not in tickers:
                    removed.append(filename[:-13])
                    os.remove(os.path.join(root, filename))
        return removed

    def filter_quotes(self, tickers):
        """
        In quotes folder, delete the files not in S&P500 list
        """
        removed = []
        for root, dirs, files in os.walk(self.quotesDir):
            for filename in files:
                if filename[:-13] not in tickers:
                    removed.append(filename[:-13])
                    os.remove(os.path.join(root, filename))
        return removed

    def filter(self):
        """
        Get S&P500 tickers and filter out the ones not in the list
        """
        tickers = self.get_SP500_tickers()
        removed_trades = self.filter_trades(tickers)
        removed_quotes = self.filter_quotes(tickers)

        print('Removed trades:', removed_trades)
        print('Removed quotes:', removed_quotes)
