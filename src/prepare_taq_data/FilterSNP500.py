import pandas as pd

df = pd.read_excel('../data/s&p500.xlsx', sheet_name='WRDS', usecols='H')
tickers = df.iloc[:, 0].unique()



print(type(tickers))
