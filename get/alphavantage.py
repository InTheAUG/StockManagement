# TODO: Build statistics method for Stock
# TODO: getetf; getindexes;
import os
import time

import numpy as np
import pandas as pd
import requests

from analysis.tech_analysis import buildtechanalysis
from utils.build import initialize_env, remove_env
from common import FILEPATHS, SAVEPATH, MODELS, STOCKFILES, ALPHAVANTAGE_KEY_VAR

# =======================HELPER FUNCTIONS=======================#


def reverse_df(df):
    """
    :type df: pandas.DataFrame containing index labelled 'timestamp' in yyyy-mm-dd-format
    """
    return df.iloc[::-1]


def getsector(save_log=False):
    data = {
        'function': 'sector',
        'apikey': os.getenv('ALPHAVANTAGE_API_KEY')
    }

    response = requests.get("https://www.alphavantage.co/query",
                            params=data, timeout=8)

    if response.status_code != 200:
        raise LookupError("[-]Invalid server response with Code: "
                          + str(response.status_code)+"\n@Sector")

    response.encoding = "utf-8"

    if save_log:
        with open(STOCKFILES + "sector.log", 'a') as f:
            f.write(response.content.decode("utf-8"))
    with open(STOCKFILES + "sector.json", 'w') as f:
        f.write(response.text)

    return


"""
Defines a Stock symbol bought at a certain price compared
   @param symbol: Stock symbol 
   @param size: "compact" = last 100 values, "full"= full available range
   @param mode: Size of returned output "TIME_SERIES_INTRADAY", "TIME_SERIES_DAILY_ADJUSTED"
  WARNING: Size, interval & mode arguments have to be referenced as keyword arguments (improves readability)

   Further information: 
   https://www.alphavantage.co/documentation/
"""


def getstock(symbol, size="compact",
             interval="15min", mode="TIME_SERIES_DAILY_ADJUSTED", save_log=False):

    key = os.getenv(ALPHAVANTAGE_KEY_VAR, False)
    if not key:
        initialize_env()
        key = os.getenv(ALPHAVANTAGE_KEY_VAR)

    data = {
                "function": mode,
                "symbol": symbol,
                "outputsize": size,
                "datatype": "csv",
                "apikey": key,
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
        with open(STOCKFILES + symbol + ".log", 'a') as f:
            f.write(response.content.decode("utf-8"))

    with open(STOCKFILES + symbol + ".csv", 'w') as f:
        f.write(response.text)

    return


def getstocklist(namelist, size='compact', interval='15min', mode="TIME_SERIES_DAILY_ADJUSTED", save_log=False,
                 freq=12):
    for name in namelist:
        getstock(name, size=size, interval=interval, mode=mode, save_log=save_log)
        time.sleep(freq)


def append_col_names(df, exclude, append_val):

    col_list = list(df.columns)

    if isinstance(exclude, list):
        for val in exclude:
            col_list.remove(val)
    else:
        col_list.remove(exclude)

    val_dict = dict(zip(col_list, [x + '_{}'.format(append_val) for x in col_list]))
    df.rename(columns=val_dict, inplace=True)

    return df


def build_df():

    files = os.listdir(STOCKFILES)
    if not files:
        return None

    stocks = [x for x in files if '.csv' in x]

    df = reverse_df(pd.read_csv(STOCKFILES + stocks[0]))
    df = append_col_names(buildtechanalysis(df), 'timestamp', stocks[0].split('.')[0])

    for stock in stocks[1:]:
        current = append_col_names(buildtechanalysis(reverse_df(pd.read_csv(STOCKFILES + stock))), 'timestamp',
                                              stock.split('.')[0])
        df = df.merge(current, sort=True, how='outer', on='timestamp')

    df.set_index('timestamp', inplace=True)

    return df
