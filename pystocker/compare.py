"""Comparison utilities for multiple stocks."""
import pandas as pd
from .core import getAllData

def compareStocks(stocks, metric='Close'):
    frames = {}
    for s in stocks:
        df = getAllData(s)
        if 'Date' in df.columns and metric in df.columns:
            df2 = df[['Date', metric]].copy()
            df2 = df2.rename(columns={metric: s})
            frames[s] = df2.set_index('Date')[s]
    if not frames:
        return pd.DataFrame()
    merged = pd.concat(frames.values(), axis=1)
    return merged

def correlateStocks(stock1, stock2):
    df1 = getAllData(stock1).set_index('Date')
    df2 = getAllData(stock2).set_index('Date')
    joined = df1['Close'].join(df2['Close'], how='inner', lsuffix='_1', rsuffix='_2')
    return joined['Close_1'].pct_change().corr(joined['Close_2'].pct_change())
