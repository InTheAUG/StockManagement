# Add Analysis for technical indicators
# Based on analysis add buy-signals if long-term-trends are established
# Based on analysis add sell-signals if long-term-trends are established
# Calculate profit-margins based on different tax models

import numpy as np
import pandas as pd

TIMEDELTAS = [7, 12, 26, 30, 90, 180]
ADCL = 'adjusted_close'

"""
Adds additional columns to AlphaVantage-Dataframe 
@param df pandas.Dataframe containing column including an adjusted close column labeled 'adjusted_close' 
"""

# TODO:Technical indicators Weighted Moving Average? VWAP? ADX? Chaikin AD? Integrate Sector performance (from
#      AlphaVantage? => more markets than US; QUANDL? )

def sma(df):
        
    for delta in TIMEDELTAS:
        df['SMA' + str(delta)] = df[ADCL].rolling(window=delta).mean()
    return df


def ema(df):
    for delta in TIMEDELTAS:
        if "SMA"+str(delta) not in df:
            df = sma(df)
        pass

    for delta in TIMEDELTAS:
        colname = 'EMA' + str(delta)
        df[colname] = df[ADCL].ewm(span=delta, min_periods=delta).mean()

    return df


def macd(df):
    if 'EMA12' and 'EMA26' in df:
        pass
    else:
        df = ema(df)

    df['MACD'] = df['EMA12'] - df['EMA26']

    return df


if __name__ == "__main__":
    df = pd.DataFrame([x for x in range(0, 100)] + [100]*100)

    df[ADCL] = df[0]
    print(macd(df))
