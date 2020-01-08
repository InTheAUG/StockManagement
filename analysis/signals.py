"""Stub to process a pd.DataFrame containing stock information and extracting buy/sell-signals"""
from . import tech_analysis as t_a


def regime_sig(df):
    if 'Regime' not in df:
        t_a.regime(df)

    vals = df['Regime'][-10:].value_count()

    if vals['1'] > vals['-1'] and vals['1'] > vals['0']:
        return 1
    elif vals['-1'] > vals[1] and vals[-1] > vals['0']:
        return -1
    else:
        return 0
