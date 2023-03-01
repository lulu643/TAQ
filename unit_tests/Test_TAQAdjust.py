from src.prepare_taq_data.TAQAdjust import TAQAdjust
import pandas as pd
import matplotlib.pyplot as plt
from src import MyDirectories

OUTPUT=MyDirectories.getTempDir()+"/output"
taq_adjust = TAQAdjust()
#this will output a csv called "NVDA_20070619-20070621_trades.csv" in the taq/output folder
taq_adjust.adjust_trade_price_and_vol("NVDA", startDateString="20070619", endDateString="20070621")
csv_path=OUTPUT+"/NVDA_20070619-20070621_trades.csv"
csv_path_2=OUTPUT+"/NVDA_20070619-20070621_quotes.csv"

df_trade=pd.read_csv(csv_path)
print(df_trade)

plt.plot(df_trade["original price"],label="original price")
plt.plot(df_trade["adjusted price"],label="adjusted price")
plt.ylabel("price")
plt.xlabel("tick")
plt.legend()
plt.title("original price/adjusted price of NVDA")

taq_adjust.adjust_quote_price_and_vol("NVDA", startDateString="20070619", endDateString="20070621")
df_quote=pd.read_csv(csv_path_2)
print(df_quote)

plt.show()
