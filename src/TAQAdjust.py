import pandas as pd
import numpy as np
from collections import defaultdict


import MyDirectories
from FileManager import FileManager


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

    def adjust_trade_price_and_vol(self, ticker, startDateString="20070919", endDateString="20070921"):
        # only return the adjusted price of the input ticker
        prices_and_vols=pd.DataFrame()


        fm = FileManager(self.baseDir)
        tradeDates = fm.getTradeDates(startDateString, endDateString)
        tradeDates.sort()
        from datetime import datetime, timedelta

        def milliseconds_to_datetime(milliseconds, date_str):
            # Parse the date string and convert it to a datetime object
            date = datetime.strptime(date_str, '%Y%m%d').date()
    
            # Convert milliseconds to a timedelta object
            delta = timedelta(milliseconds=milliseconds)
    
            # Create a datetime object representing the start of the day
            start_of_day = datetime.combine(date, datetime.min.time())
    
            # Add the timedelta object to the start of the day datetime object
            result = start_of_day + delta  
            return result

        for date_index in range(len(tradeDates)):
            date=tradeDates[date_index]
            trade_file = fm.getTradesFile(date, ticker)
            # add to original price dictionary
            for i in range(trade_file.getN()):
                trade_price=trade_file.getPrice(i)
                time=milliseconds_to_datetime(milliseconds=trade_file.getMillisFromMidn(i), date_str=date)
                prices_and_vols.loc[time,"original price"]=trade_price
                adj_price = self.adjust_value(self._adjust_factor_price, time.date().strftime('%Y-%m-%d'), ticker, trade_price)
                prices_and_vols.loc[time,"adjusted price"]=adj_price
                
                trade_vol=trade_file.getSize(i)
                prices_and_vols.loc[time,"original vol"]=trade_vol
                adj_vol = self.adjust_value(self._adjust_factor_vol, time.date().strftime('%Y-%m-%d'), ticker, trade_vol)
                prices_and_vols.loc[time,"adjusted vol"]=adj_vol
                



if __name__ == "__main__":
    taq_adjust = TAQAdjust()
    taq_adjust.adjust_trade_price_and_vol("IBM")

