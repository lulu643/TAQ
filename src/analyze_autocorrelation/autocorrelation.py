from src.compute_summary_stats.Stats import ret_trade
import statsmodels.api as sm
# part 3(a), find the buck_size
def buck_test(df,k=10):
    for x in range(1,300):
        ret = ret_trade(df,x).dropna()
        if sm.stats.acorr_ljungbox(ret, lags=[k], return_df=True)["lb_pvalue"].to_list()[0] > 0.05:
            buck_size = x
            break
        else:
            continue
    return buck_size

# part 3(b), check the stationary
def adf_test(df):
    buck_size = buck_test(df)
    ret = ret_trade(df,buck_size).dropna()
    p_value = sm.tsa.stattools.adfuller(ret)[1]
    if p_value < 0.05:
        print("Stationary")
    else:
        print("Not Stationary")
    return p_value