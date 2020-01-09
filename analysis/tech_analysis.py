"""Provides interface for technical analysis parameteres based on a pd.DataFrame"""

#TODO:
# Add Analysis for technical indicators
# Based on analysis add buy-signals if long-term-trends are established
# Based on analysis add sell-signals if long-term-trends are established
# Calculate profit-margins based on different tax models

import numpy as np
import pandas as pd

TIMEDELTAS = [7, 12, 26, 30, 90, 180, 270]
ADCL = 'adjusted_close'

"""
Adds additional columns to AlphaVantage-Dataframe 
@param df pandas.Dataframe containing column including an adjusted close column labeled 'adjusted_close' 
"""

# TODO:Technical indicators Weighted Moving Average? VWAP? ADX? Chaikin AD? Integrate Sector performance (from
#      AlphaVantage? => more markets than US; QUANDL? )


def returns(df):
    df['Change1'] = df[ADCL].shift(-1) - df[ADCL]
    df['Return1'] = (df['Change1'] / df[ADCL]) * 100

    for delta in TIMEDELTAS:
        df['Change' + str(delta)] = df[ADCL].shift(-delta) - df[ADCL]
        df['Return' + str(delta)] = (df['Change' + str(delta)] / df[ADCL]) * 100

    return df


def sma(df):
    for delta in TIMEDELTAS:
        df['SMA' + str(delta)] = df[ADCL].rolling(window=delta).mean()
    return df


def ema(df):
    for delta in TIMEDELTAS:
        if "SMA"+str(delta) not in df:
            df = sma(df)
        colname = 'EMA' + str(delta)
        df[colname] = df[ADCL].ewm(span=delta, min_periods=delta).mean()

    return df


def macd(df):
    if 'EMA12' not in df or 'EMA26' not in df:
        df = ema(df)
    df['MACD'] = df['EMA12'] - df['EMA26']

    df['MACD_long'] = df['EMA30'] - df['EMA270']

    return df


def regime(df, deviation=50):
    if 'MACD_long' not in df:
        macd(df)

    df['Regime'] = np.where(df['MACD_long'] > deviation, 1, 0)
    df['Regime'] = np.where(df['MACD_long'] < -deviation, -1, df['Regime'])

    return df


def buildtechanalysis(df):
    df = regime(df)
    df = returns(df)


    return df
