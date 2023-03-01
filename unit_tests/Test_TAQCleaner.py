from src.prepare_taq_data.TAQCleaner import clean_trade
import pandas as pd
from src import MyDirectories

# to minimize runtime, select part of the data to clean

OUTPUT=MyDirectories.getTempDir()+"/output"
csv_path=OUTPUT+"/NVDA_20070619-20070621_trades.csv"


df=pd.read_csv(csv_path)[:1000]
print(df)
print(clean_trade(df,100,0.00001*df["adjusted price"].mean())["adjusted price"])
#graphs that showing the function works is in the write up
#and note that their length are different

