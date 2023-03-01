import numpy as np
import pandas as pd
#k is the number of ticks (not days)
def clean_trade(df,k,gamma):
    df_trade=df.copy()
    df["mean"] = df_trade["adjusted price"].rolling(k).mean()
    df["std"] = df_trade["adjusted price"].rolling(k).std()
    mean_temp=df_trade[:k+2]["adjusted price"].mean()
    std_temp=df_trade[:k+2]["adjusted price"].std()
    df["mean"]=df["mean"].fillna(mean_temp)
    df["std"]=df["std"].fillna(std_temp)
    for index, row in df.iterrows():
        if(abs(row["mean"]-row["adjusted price"])>2*row["std"]+gamma):
            df_trade.iloc[index, :] = None
    df_trade = df_trade.dropna().reset_index(drop=True)
    return df_trade
