"""
Created on: 2nd Aug 19
Author: Dencan Gan

Script for scraping daily btc prices from coin market cap.
"""

from utils import soupify
from database import Database
from utils import char_to_date
from datetime import datetime
import pandas as pd


class Crypto:

    def __init__(self, crypto):
        self.crypto = crypto
        self.labels = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Market Cap']
        self.pattern = 'td'

    def historic_data(self, start_date=None, end_date=datetime.today().strftime('%Y%m%d')):
        """Pulls specific historical cryptocurrency data from coin market cap and uploads to mongodb.

        Args:
            start_date (str): Start date of period. Acceptable type, yyyymmdd.
            end_date (str): End date, defaults to today.

        Returns:
            d (dict): Dictionary of historical crypto data

        Notes:
            If no start date is found for a specific cryptocurrency, it will return the one-month of historical data
        """

        default_link = r'https://coinmarketcap.com/currencies/' + self.crypto + '/historical-data/'

        if start_date is None:
            custom_link = default_link # Using coinmarketcap default page (1 month data)

        else:
            custom_link = default_link + '?start=' + start_date + '&end=' + end_date

        soup = soupify(url=custom_link) # Pulling html

        historic_data = []
        for x in (soup.select(self.pattern)):
            historic_data.append(x.text)

        data = {}
        for i, e in enumerate(self.labels):
            data[e] = historic_data[i::7]

        df = pd.DataFrame(data)

        df_ctd = char_to_date(s=df).sort_values('Date')
        df_ctd = df_ctd.set_index('Date')

        # library = mongodb_connect(secret_dir=r'C:\Users\Dencan Gan\secret\mongo_credentials.json',
        #                           db_name='crypto', lib_name='bitcoin')
        #
        # composite_list = [historic_data[x:x + 7] for x in range(0, len(historic_data), 7)]
        #
        # for i in range(len(composite_list)):
        #     day_data = dict(zip(self.labels, composite_list[i][0:7]))
        #     library.insert_one(day_data)

        return df_ctd

    def daily_data(self):
        """Daily scrap function
        """
        link = r'https://coinmarketcap.com/currencies/' + self.crypto + '/historical-data/'

        soup = soupify(url=link)  # Pulling html

        historic_data = []

        for x in (soup.select(self.pattern)):
            print(x.text)
            historic_data.append(x.text)

        day_data = dict(zip(self.labels, historic_data[0:7]))

        df = pd.DataFrame(day_data, index=[0])

        df_ctd = char_to_date(s=df).sort_values('Date')
        df_ctd = df_ctd.set_index('Date')

        return df_ctd

        #library.insert_one(day_data)


if __name__ == '__main__':
    scrape = Crypto(crypto='bitcoin') # Initialise crypto class and crypto to scrape
    database = Database()
    library = database.mongodb_connect(db_name='arctic', lib_name='bitcoin') # Connect to appropriate mongodb to store data
    # b = scrape.historic_data()
    c = scrape.daily_data()

    library.append('bitcoin', c, upsert=True)

    # database.arctic_write(symbol_name='bitcoin', lib_name='bitcoin', df=b)

    df = database.arctic_read(symbol_name='bitcoin')
    # x = library.find({'Date': 'Dec 17, 2019'})
    #
    # for i in x:
    #     print(i)





