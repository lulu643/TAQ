from src.compute_summary_stats import Stats
import pandas as pd
from src import MyDirectories

OUTPUT=MyDirectories.getTempDir()+"/output"
#use smaller dataset to minimize runtime
csv_path=OUTPUT+"/NVDA_20070619-20070621_trades.csv"
df=pd.read_csv(csv_path)
five_min_returns=Stats.ret_trade(df,5*60)
print(five_min_returns)
return_stats=Stats.ret_stats(five_min_returns,5*60)
print(return_stats)

csv_path2=OUTPUT+"/IBM_20070919-20070921_quotes.csv"
df2=pd.read_csv(csv_path2)
five_min_return_quotes=Stats.ret_quote(df2,5*60)
print(five_min_return_quotes)

print(Stats.stats(df,df2,5*60))


