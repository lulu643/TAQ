import pandas as pd
import numpy as np
from collections import defaultdict

from src import MyDirectories
from src.FileManager import FileManager

OUTPUT=MyDirectories.getTempDir()+"/output"

class TAQAdjust:
    def __init__(self):
        self.baseDir = MyDirectories.getTAQDir()
        self.adjFactorPath = self.baseDir + '/s&p500.xlsx'
        self._adjust_factor_price = self.read_adjust_factors('price')
        self._adjust_factor_price.to_csv("temp.csv")
        self._adjust_factor_vol = self.read_adjust_factors('vol')

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
        table = pd.pivot_table(df, index='Names Date', columns='Ticker Symbol', fill_value=np.nan)
        table.columns = table.columns.droplevel()
        table.index = pd.to_datetime(table.index.astype(int), format='%Y%m%d')
        return table

    def adjust_value(self, adjust_factor, trade_date, ticker, value):
        contem_factor = adjust_factor.loc[trade_date, ticker]
        last_factor = adjust_factor[ticker].iloc[-1]
        return value / contem_factor * last_factor

    # def adjust_trade_price_and_vol(self, ticker, startDateString="20070919", endDateString="20070921"):
    #     # only return the adjusted price of the input ticker
    #     prices_and_vols=pd.DataFrame()

    #     fm = FileManager(self.baseDir)
    #     tradeDates = fm.getTradeDates(startDateString, endDateString)
    #     tradeDates.sort()
    #     from datetime import datetime, timedelta

    #     def milliseconds_to_datetime(milliseconds, date_str):
    #         # Parse the date string and convert it to a datetime object
    #         date = datetime.strptime(date_str, '%Y%m%d').date()

    #         # Convert milliseconds to a timedelta object
    #         delta = timedelta(milliseconds=milliseconds)

    #         # Create a datetime object representing the start of the day
    #         start_of_day = datetime.combine(date, datetime.min.time())

    #         # Add the timedelta object to the start of the day datetime object
    #         result = start_of_day + delta
    #         return result

    #     for date_index in range(len(tradeDates)):
    #         date=tradeDates[date_index]
    #         trade_file = fm.getTradesFile(date, ticker)
    #         # add to original price dictionary
    #         for i in range(trade_file.getN()):
    #             trade_price=trade_file.getPrice(i)
    #             time=milliseconds_to_datetime(milliseconds=trade_file.getMillisFromMidn(i), date_str=date)
    #             prices_and_vols.loc[time,"original price"]=trade_price
    #             adj_price = self.adjust_value(self._adjust_factor_price, time.date().strftime('%Y-%m-%d'), ticker, trade_price)
    #             prices_and_vols.loc[time,"adjusted price"]=adj_price

    #             trade_vol=trade_file.getSize(i)
    #             prices_and_vols.loc[time,"original vol"]=trade_vol
    #             adj_vol = self.adjust_value(self._adjust_factor_vol, time.date().strftime('%Y-%m-%d'), ticker, trade_vol)
    #             prices_and_vols.loc[time,"adjusted vol"]=adj_vol

    #     prices_and_vols.to_csv("IBM_0919-0921.csv")

    def adjust_trade_price_and_vol(self, ticker, startDateString="20070919", endDateString="20070921"):
        # only return the adjusted price of the input ticker

        fm = FileManager(self.baseDir)
        tradeDates = fm.getTradeDates(startDateString, endDateString)
        tradeDates.sort()

        num_rows = 0
        for date in tradeDates:
            trade_file = fm.getTradesFile(date, ticker)
            num_rows += trade_file.getN()

        prices_and_vols = pd.DataFrame(index=range(num_rows),
                                       columns=["date", "milisecond from midnight", "original price", "adjusted price",
                                                "original vol", "adjusted vol"])
        print(prices_and_vols)
        from datetime import datetime

        sum = 0
        for date in tradeDates:
            trade_file = fm.getTradesFile(date, ticker)
            for i in range(trade_file.getN()):
                trade_price = trade_file.getPrice(i)
                prices_and_vols.iloc[sum].loc["date"] = datetime.strptime(date, '%Y%m%d')
                prices_and_vols.iloc[sum].loc["milisecond from midnight"] = trade_file.getMillisFromMidn(i)
                prices_and_vols.iloc[sum].loc["original price"] = trade_price
                adj_price = self.adjust_value(self._adjust_factor_price,
                                              datetime.strptime(date, '%Y%m%d').strftime('%Y-%m-%d'), ticker,
                                              trade_price)
                prices_and_vols.iloc[sum].loc["adjusted price"] = adj_price

                trade_vol = trade_file.getSize(i)
                prices_and_vols.iloc[sum].loc["original vol"] = trade_vol
                adj_vol = self.adjust_value(self._adjust_factor_vol,
                                            datetime.strptime(date, '%Y%m%d').strftime('%Y-%m-%d'), ticker, trade_vol)
                prices_and_vols.iloc[sum].loc["adjusted vol"] = adj_vol
                sum += 1
        csv_path = OUTPUT+"/{}_{}-{}_trades.csv".format(ticker, startDateString, endDateString)
        prices_and_vols.to_csv(csv_path)

    def adjust_quote_price_and_vol(self, ticker, startDateString="20070919", endDateString="20070921"):
        # only return the adjusted price of the input ticker
        fm = FileManager(self.baseDir)
        tradeDates = fm.getTradeDates(startDateString, endDateString)
        tradeDates.sort()

        num_rows = 0
        for date in tradeDates:
            trade_file = fm.getQuotesFile(date, ticker)
            num_rows += trade_file.getN()

        prices_and_vols = pd.DataFrame(index=range(num_rows),
                                       columns=["date", "milisecond from midnight", "adjusted ask price",
                                                "adjusted ask vol", "adjusted bid price", "adjusted bid vol"])
        print(prices_and_vols)
        from datetime import datetime

        sum = 0
        for date in tradeDates:
            trade_file = fm.getQuotesFile(date, ticker)
            for i in range(trade_file.getN()):
                print(sum)
                ask_price = trade_file.getAskPrice(i)
                bid_price = trade_file.getBidPrice(i)
                ask_size = trade_file.getAskSize(i)
                bid_size = trade_file.getBidSize(i)
                prices_and_vols.iloc[sum].loc["date"] = datetime.strptime(date, '%Y%m%d').date()
                prices_and_vols.iloc[sum].loc["milisecond from midnight"] = trade_file.getMillisFromMidn(i)
                adj_ask_price = self.adjust_value(self._adjust_factor_price,
                                                  datetime.strptime(date, '%Y%m%d').strftime('%Y-%m-%d'), ticker,
                                                  ask_price)
                prices_and_vols.iloc[sum].loc["adjusted ask price"] = adj_ask_price
                adj_bid_price = self.adjust_value(self._adjust_factor_price,
                                                  datetime.strptime(date, '%Y%m%d').strftime('%Y-%m-%d'), ticker,
                                                  bid_price)
                prices_and_vols.iloc[sum].loc["adjusted bid price"] = adj_bid_price
                adj_ask_size = self.adjust_value(self._adjust_factor_vol,
                                                 datetime.strptime(date, '%Y%m%d').strftime('%Y-%m-%d'), ticker,
                                                 ask_size)
                prices_and_vols.iloc[sum].loc["adjusted ask vol"] = adj_ask_size
                adj_bid_size = self.adjust_value(self._adjust_factor_vol,
                                                 datetime.strptime(date, '%Y%m%d').strftime('%Y-%m-%d'), ticker,
                                                 bid_size)
                prices_and_vols.iloc[sum].loc["adjusted bid vol"] = adj_bid_size
                sum += 1

        csv_path = OUTPUT+"/{}_{}-{}_quotes.csv".format(ticker, startDateString, endDateString)
        prices_and_vols.to_csv(csv_path)

if __name__ == "__main__":
    taq_adjust = TAQAdjust()
    taq_adjust.adjust_trade_price_and_vol("IBM")


