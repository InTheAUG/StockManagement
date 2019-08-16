# TODO: Implement ETF class
# TODO: Build statisitics method for Stock
# TODO: getsector; getetf; getindexes;

import os
import time
import requests
import numpy as np
import pandas as pd

from analysis import analysis
from bs4 import BeautifulSoup as BSoup

# =======================HELPER FUNCTIONS=======================#


def reverse_df(df):
    """
    :type df: pandas.DataFrame containing index labelled 'timestamp' in yyyy-mm-dd-format
    """
    first = df['timestamp'][0]
    last = df['timestamp'][-1]
    first = [int(x) for x in first.split("-")] 
    last = [int(x) for x in last.split("-")] 

    if first[0] > last[0]: 
        df = df.iloc[::-1]
    elif first[1] > last[1]: 
        df = df.iloc[::-1]
    elif first[2] > last[2]: 
        df = df.iloc[::-1]

    return df


def getsector(save_log=False):
    data = {
        'function': 'sector',
        'apikey': os.environ['ALPHAVANTAGE_API_KEY']
    }

    response = requests.get("https://www.alphavantage.co/query",
                            params=data, timeout=8)

    if response.status_code != 200:
        raise LookupError("[-]Invalid server response with Code: "
                          + str(response.status_code)+"\n@Sector")

    response.encoding = "utf-8"

    if save_log:
        with open("/var/stock/sector.log", 'a') as f:
            f.write(response.content.decode("utf-8"))
    with open("/var/stock/sector.json", 'w') as f:
        f.write(response.text)

    df = pd.read_json("/var/stock/sector.json")

    del df['Meta Data']
    df.dropna(inplace=True)
    df.interpolate(axis=0,inplace=True)

    return df


"""
Defines a Stock symbol bought at a certain price compared
   @param symbol: Stock symbol 
   @param size: "compact" = last 100 values, "full"= full available range
   @param mode: Size of returned output "TIME_SERIES_INTRADAY", "TIME_SERIES_DAILY_ADJUSTED"
  WARNING: Size, interval & mode arguments have to be referenced as keyword arguments (improves readability)

   Further information: 
   https://www.alphavantage.co/documentation/
"""


def getstock(symbol, *, size="compact",
             interval="15min", mode="TIME_SERIES_DAILY_ADJUSTED", save_log=0):

    data = { 
                "function": mode,
                "symbol": symbol,
                "outputsize": size,
                "datatype": "csv",
                "apikey": os.environ['ALPHAVANTAGE_API_KEY'],
                }
    if mode == "TIME_SERIES_INTRADAY": 
        data['interval'] = interval

    response = requests.get("https://www.alphavantage.co/query", 
                            params=data, timeout=8)
 
    if response.status_code != 200: 
        raise LookupError("[-]Invalid server response with Code: "
                          + str(response.status_code)+"\n@Symbol: " + symbol)
    
    response.encoding = "utf-8"
    
    # Save entire response if logging is enabled
    if save_log: 
        with open("/var/stock"+symbol+".log", 'a') as f:
            f.write(response.content.decode("utf-8")) 
    with open("/var/stock/"+symbol+".csv", 'w') as f: 
        f.write(response.text)

    data_read = False

    while not data_read:  
        try: 
            df = pd.read_csv("/var/stock/"+symbol+".csv")
            df.index = df['timestamp']
            df = reverse_df(df)
            del df['timestamp']
            data_read = True
            df.interpolate(axis=0, inplace=True)

            return df

        # TODO: Inspect why df.index throws key-error on inconsistent basis
        except KeyError: 
            time.sleep(5)
            continue 


# ======================================================================#


class Stock:

    # Stock metadata
    __symbol: str = ""
    __name: str = ""
    __market: str = ""
    __sector: str = ""

    # Stock price variables
    __initial: int = 0
    __diff: float = 0
    __amount: float = 0
    __pieces: int = 0

    # Dataframe
    __df = None 
    
    """
    @param symbol = Stock symbol
    @param market = current stock exchange
    @param date = date of purchase in format 'yyyy-mm-dd'
    """
    def __init__(self, symbol, price, pieces, market, sector):
        self.__symbol = symbol
        self.__market = market
        self.__sector = sector
        self._getname(self.__symbol)

        self.update_df() 

        self.__pieces = pieces
        self.__initial = price
        self.__amount = self.__initial * self.__pieces
        self.__diff = (self.__df['adjusted_close'][-1]/self.__initial - 1) * 100

    def __repr__(self):
        return self.__symbol+"_Stock"

    def __str__(self):
        return self.__symbol

    def _getname(self, symbol):
        r = requests.get("https://finance.yahoo.com/quote/"+symbol, timeout=2)
        soup = BSoup(r.text, features='lxml')
        self.__name = soup.title.text.split("Stock")[0]
        return 

    def curr_difference(self): 
        df = getstock(self.__symbol)
        self.__diff = (df['adjusted_close'][-1]/self.__initial - 1) * 100

        return self.__diff

    def update_df(self): 
        try: 
            self.__df = getstock(self.__symbol, size="full")
        except LookupError:
            time.sleep(5)
            try: 
                self.__df = getstock(self.__symbol, size="full")
            except Exception:
                pass
        except requests.exceptions.Timeout:
            print("Stock Update failed")
            return

        self.statistics()

    def information(self): 
        name = self.__name.center(30).center(72, "=")
        print(name)
        print("Current volume:", str(self.__amount), '\n',
              "Bought at:", str(self.__initial), '\n',
              "Percentage change:", str(round(self.curr_difference(), 3))+"%\n")
        
    def new_inv(self, price, pieces):
        addition = price * pieces 
        origin = self.__amount 
        total_amount = origin + addition
        total_pieces = self.__pieces + pieces

        self.__pieces = total_pieces 
        self.__amount = total_amount
        self.__initial = total_amount / total_pieces

    def compare_sector(self, sector_df):
        try:
            entries = sector_df.loc[self.__sector]
        except KeyError:
            print("[-] Error at "+self.__name+" compare_sector: self.__sector: \""+self.__sector+"\" not found")
            return




    def statistics(self):
        self.__df = analysis.macd(self.__df)
        # TODO: Incorporate other analysis params
        # TODO: Add plotting

    def signals(self):
        signals = {}
        self.statistics()
        pass
        # return signals
        # TODO: build buy/sell signals from statistics
