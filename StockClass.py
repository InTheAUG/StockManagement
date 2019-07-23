import os 
import numpy as np 
import pandas as pd 
import requests
from bs4 import BeautifulSoup as BSoup
from enum import Enum
import time

#===============================HELPER FUNCTIONS========================#
def reverse_df(df): 

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
#=======================================================================#

"""Defines a Stock symbol bought at a certain price compared
   @param symbol: Stock symbol 
   @param size: "compact" = last 100 values, "full"= full available range
   @param mode: Size of returned output "TIME_SERIES_INTRADAY", "TIME_SERIES_DAILY_ADJUSTED"
  WARNING: Size & mode arguments have to be referenced as keyword arguments (improves readability)

   Further information: 
   https://www.alphavantage.co/documentation/
"""
def getstock(symbol*,size="compact",interval ="15min",mode="TIME_SERIES_DAILY_ADJUSTED"): 
    API_URL = "https://www.alphavantage.co/query"
    data = { 
            "function":mode,
            "symbol": symbol,
            "outputsize":size,
            "datatype":"csv",
            "apikey": os.environ['ALPHAVANTAGE_API_KEY'],
            }
    if mode == "TIME_SERIES_INTRADAY": 
        data = { 
                "function":mode,
                "symbol": symbol,
                "interval":interval
                "outputsize":size,
                "datatype":"csv",
                "apikey": os.environ['ALPHAVANTAGE_API_KEY'],
                }

    response = requests.get(API_URL, params=data)
    response.encoding="utf-8"

    if response.status_code != 200: 
        raise LookupError("[-]@getstock Value not found: "+symbol)

    with open("/var/stock/"+symbol+".csv", 'w') as f: 
        f.write(response.text)
    data_read = False

    while not data_read:  
        try: 
            df = pd.read_csv("/var/stock/"+symbol+".csv")
            df.index = df['timestamp']
            df = reverse_df(df)
            data_read = True

        except KeyError: 
            time.sleep(5)
            continue 

    del df['timestamp']

    return df


class Stock:  
    #Stock metadata
    __symbol = ""
    __name = ""
    __market= ""

    #Stock price variables
    __initial = 0 
    __diff = 0
    __amount = 0 
    __pieces = 0 

    #Dataframe 
    __df = None 
    
    """
    @param symbol = Stock symbol
    @param market = current stock exchange
    @param date = date of purchase in format 'yyyy-mm-dd'
    """
    def __init__(self,symbol,price,pieces,market, date): 
        self.__symbol = symbol
        self.__market = market
        self.getname(self.__symbol)

        self.update_df() 

        self.__pieces = pieces
        self.__initial = price
        self.__amount = self.__initial * self.__pieces
        self.__diff = (self.__df['adjusted_close'][-1]/self.__initial -1) * 100

    def __repr__(self): 
        return self.__symbol+"_Stock"

    def __str__(self): 
        return self.__symbol

    def getname(self,symbol): 
        r = requests.get("https://finance.yahoo.com/quote/"+symbol)
        soup = BSoup(r.text, features="lxml")
        self.__name = soup.title.text.split("Stock")[0]


    """
    Return the current increase/decrease based on initial investment in percent 
    """
    def curr_difference(self): 
        df = getstock(self.__symbol)
        self.__diff = (df['adjusted_close'][-1]/self.initial -1) * 100 

        return self.__diff

    def update_df(self): 
        self.__df = getstock(self.__symbol, size="full")
        self.statistics()

    def statistics(self): 
        timedeltas = [7,30,90,180,365]
        
        for delta in timedeltas: 
            self.__df['MovAvg_'+ str(delta)+'d'] = self.__df['adjusted_close'].rolling(window=delta).mean()


    def information(self): 
        name = self.__name.center(30).center(72,"=")
        print(name)
        print("Current volume:",str(self.__amount),"\n",
             "Bought at:", str(self.__initial), "\n",
             "Percentage change:",str(round(self.__diff,3)+"%\n")
        
    def update_new_inv(self,price,pieces): 
        addition = price * pieces 
        origin = self.__amount 
        total_amount = origin + addition
        total_pieces = self.__pieces + pieces

        self.__pieces = total_pieces 
        self.__amount = total_amount
        self.__initial = total_amount / total_pieces
            
            
            
if __name__ =="__main__": 
