import os
import pandas as pd
from src import MyDirectories


class FilterSP500:
    def __init__(self):
        self.baseDir = MyDirectories.getTAQDir()
        self.tradesDir = MyDirectories.getTradesDir()
        self.quotesDir = MyDirectories.getQuotesDir()
        # self.baseDir = "/Users/sihanliu/Desktop/AlgoTradingCourse/taq/data/"
        # self.tradesDir = "/Users/sihanliu/Desktop/full_datasets/full_unzipped_raw/trades"
        # self.quotesDir = "/Users/sihanliu/Desktop/full_datasets/full_unzipped_raw/quotes"

    def get_SP500_tickers(self):
        """
        Get all S&P500 tickers from the Excel given
        """
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

    def save_removed_ticker_lst(self, lst, filename):
        with open(filename, 'w') as f:
            for line in lst:
                f.write(f"{line}\n")

    def filter(self):
        """
        Get S&P500 tickers and filter out the ones not in the list
        """
        tickers = self.get_SP500_tickers()
        removed_trades = self.filter_trades(tickers)
        removed_quotes = self.filter_quotes(tickers)

        # save the removed tickers list to txt files
        self.save_removed_ticker_lst(removed_trades, 'removed_trades.txt')
        self.save_removed_ticker_lst(removed_quotes, 'removed_quotes.txt')
