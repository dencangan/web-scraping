"""Basic buy low sell high strategy

TODO write profits to json, find a way to sum
"""

import pandas as pd
import json

from utils import soupify

from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators


class Trade:

    def __init__(self, region, category):

        with open(r'C:\Users\Dencan Gan\Credentials\credentials.json') as json_cfg:
            credentials = json.load(json_cfg)

        api = credentials['alpha_vantage']['api_key']

        self.labels = ['Ticker', 'Last', '% Change', 'Change', 'Signal', 'Vol', 'Mkt Cap', 'P/E', 'EPS', 'Employees',
                       'Industry']
        self.link = 'https://www.tradingview.com/markets/stocks-' + region + '/' + category

        self.time_series = TimeSeries(api, output_format='pandas')
        self.technical_indicator = TechIndicators(api)

    def daily_data(self, stock):
        data_daily, meta_data_daily = self.time_series.get_daily(symbol=stock, outputsize='full')
        return data_daily, meta_data_daily

    def intraday_data(self, stock, interval='1min'):
        data_intraday, meta_data_intraday = self.time_series.get_intraday(symbol=stock, interval=interval, outputsize='full')
        return data_intraday, meta_data_intraday

    def simple_moving_average(self, stock):
        sma, meta_sma = self.technical_indicator.get_sma(symbol=stock)
        return sma, meta_sma

    def get_stocks(self, num_of_stocks):

        html_page = soupify(self.link)

        data = []
        for x in (html_page.select('td')):
            data.append(x.text)

        keys = {}
        for i, e in enumerate(self.labels):
            keys[e] = data[i::11]

        # Change to dataframe and format data to split name and ticker
        df = pd.DataFrame(keys)
        df['x'] = df['Ticker'].str.strip('\n').str.replace('\t', '').str.split('\n')
        df[['(new_ticker)', 'Name', '(blank)']] = pd.DataFrame(df.x.values.tolist(), index=df.index)
        df = df.drop(columns=['Ticker', '(blank)', 'x'])
        df = df.rename(columns={'(new_ticker)': 'Ticker'})

        stock_detail = df.head(num_of_stocks)[['Name', 'Ticker', 'Last', '% Change', 'Signal', 'Vol', 'Mkt Cap',
                                               'Industry']]

        tickers_lst = stock_detail['Ticker'].tolist()
        print(tickers_lst)
        return tickers_lst

    def execute(self, stock_data):

        # Starting price
        execute_price = stock_data['4. close'][0]

        for timestamp, price in stock_data.iterrows():

            # If profited before, assign next closing price and executed price
            if execute_price is None:
                execute_price = price['4. close']

            # If executed price lower than closing, we are profit making
            if execute_price < price['4. close']:
                profit = float(price['4. close'] - execute_price)
                print(timestamp, 'Profit making trade.', profit)

                # Once profited, reset executed price to 0
                execute_price = None

            # Skip and continue
            else:
                print(timestamp, 'Loss making trade.')


if __name__ == "__main__":
    trade = Trade(region='usa', category='market-movers-gainers')

    df = trade.get_stocks(num_of_stocks=3)

    df, meta = trade.intraday_data(df[0], interval='5min')
    today = df.loc['2020-01-24']
    final = today.sort_index()
    trade.execute(final)

