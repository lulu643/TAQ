import pandas as pd
import datetime
from IPython.display import display


# compute the X-sec returns for trade, part 2(a)
def ret_trade(df, x):
    p = df["date"]
    t = df["milisecond from midnight"]
    price = (df["adjusted price"] * df["adjusted vol"]).groupby([p, t]).sum() / (df["adjusted vol"]).groupby(
        [p, t]).sum()
    price.name = "avg_adj_price"
    price = price.reset_index()

    first_in_intervals = []
    quotient = -1
    dividing = x * 1000
    for index, row in price.iterrows():
        divided = row["milisecond from midnight"]
        result = int(divided / dividing)
        if (result != quotient):
            first_in_intervals.append(row["avg_adj_price"])
        quotient = result
    ret = pd.Series(first_in_intervals).pct_change()

    return ret


# compute the X-sec returns for quotes, part 2(a)
def ret_quote(df, x):
    df["mid quotes"] = (df["adjusted ask price"] + df["adjusted bid price"]) / 2
    p = df["date"]
    t = df["milisecond from midnight"]
    price = df["mid quotes"].groupby([p, t]).mean()
    price = price.reset_index()

    first_in_intervals = []
    quotient = -1
    dividing = x * 1000
    for index, row in price.iterrows():
        divided = row["milisecond from midnight"]
        result = int(divided / dividing)
        if (result != quotient):
            first_in_intervals.append(row["mid quotes"])
        quotient = result
    ret = pd.Series(first_in_intervals).pct_change()
    return ret

# given X-sec return, compute stats related to return
# method can be "compound" or "simple", which is compounded or simple annualized return
def ret_stats(ret,x,method="simple"):
    k = 3600 * 6.5 * 252/x
    if(method=="compound"):
        mean=(1+ret.mean())**(6.5*252*3600/x)-1
        median = (1+ret.median()) **(6.5*252*3600/x)-1
    else:
        mean = ret.mean() * k
        median = ret.median() * k
    std = ret.std() * (k**0.5)
    mad = ret.mad() * k
    skew = ret.skew()
    kurtosis = ret.kurtosis()
    large = ret.nlargest(10,keep = "all").to_list()
    small = ret.nlargest(10,keep = "all").to_list()
    cumret = ret.cumsum()
    drawdown = cumret - cumret.cummax()
    max_drawdown = (-drawdown).max()
    df = pd.DataFrame([mean,median,std,mad,skew,kurtosis,large,small,max_drawdown],index = ["mean","median","std","mad","skew","kurtosis","largest 10","smallest 10","max_drawdown"], columns=["basic return statistics"])
    return df

# part 2(b)
def stats(df_trade,df_quotes,x):
    length = (pd.to_datetime(df_trade["date"]).iloc[-1]-pd.to_datetime(df_trade["date"]).iloc[1]) + datetime.timedelta(days=1)
    trade_num = len(df_trade)
    quotes_num = len(df_quotes)
    frac_trade_quotes = trade_num/quotes_num
    ret_trades = ret_trade(df_trade,x)
    ret_quotes = ret_quote(df_quotes,x)
    print("For Trades:")
    ret_trade_stats = ret_stats(ret_trades,x)
    print("For Quotes:")
    ret_quotes_stats = ret_stats(ret_quotes,x)
    df = pd.DataFrame([length,trade_num,quotes_num,frac_trade_quotes],index = ["length","trade_num","quotes_num","frac_trade_quotes"], columns=["basic statistics"])
    display(df.T)