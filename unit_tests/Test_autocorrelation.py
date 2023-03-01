from src.analyze_autocorrelation import autocorrelation
import pandas as pd
from src import MyDirectories

OUTPUT=MyDirectories.getTempDir()+"/output"
#use smaller dataset to minimize runtime
csv_path=OUTPUT+"/NVDA_20070619-20070621_trades.csv"
df=pd.read_csv(csv_path)
print("optimized size is  ",autocorrelation.buck_test(df))

#check whether stationary
autocorrelation.adf_test(df)
