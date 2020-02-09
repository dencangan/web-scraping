"""
Simple analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import utils

# Config
plt.style.use('seaborn')
pd.set_option('display.max_columns', 5)


def _format_df(df, category='4. close'):
    """Format data frame"""
    return utils.char_to_date(df)[[category]]


def log_daily_returns(data):
    """Give log daily returns"""
    return data.apply(lambda x: np.log(x) - np.log(x.shift(1)))[1:]


if __name__ == '__main__':

    stocks = SelectStock(region='usa', category='market-movers-gainers')

    alpha_vantage = AlphaVantage()
    df, meta_data = alpha_vantage.daily_data(stock='MSFT')
    df = _format_df(df)

    df.columns = ['Close']

    # sma, sma_data = alpha_vantage.simple_moving_average(stock='MSFT')

    # Simple Moving Average
    rolling_mean = df.Close.rolling(window=20).mean()
    rolling_mean2 = df.Close.rolling(window=50).mean()

    plt.plot(df.Close, label='MSFT')
    plt.plot(rolling_mean, label='AMD 20 Day SMA', color='orange')
    plt.plot(rolling_mean2, label='AMD 50 Day SMA', color='magenta')
    plt.legend(loc='upper left')
    plt.show()

    df_log_returns = log_daily_returns(df)


