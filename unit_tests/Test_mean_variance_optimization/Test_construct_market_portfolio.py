from src.mean_variance_optimization.construct_market_portfolio import ConstructMarketPortfolio


def test_construct_market_portfolio_main():
    # initiate an object
    my_obj = ConstructMarketPortfolio()

    # TEST1: test the method "get_the_weight"
    # expected return:  a dataframe
    #                   index of dataframe: ticker symbols
    #                   column of dataframe: ['Date', 'Price', 'SharesOutStanding', 'MarketCap', 'Weight']
    date1 = '2007-06-20'
    weights = my_obj.get_the_weights(date1)
    print(f'Here is the weight of the stocks in market portfolio on date {date1}:')
    print(weights)

    # TEST2: test the method "compute_turnover"
    date2 = '2007-09-20'
    print(f'Here is the turnover ratio between the market portfolio on {date1} and {date2}:')
    print(round(my_obj.compute_turnover(date1, date2), 2))


if __name__ == "__main__":
    test_construct_market_portfolio_main()
