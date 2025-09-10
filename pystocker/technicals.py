"""Technical indicators implemented in pure pandas/numpy (no external ta lib)"""
import pandas as pd
import numpy as np

def getMovingAverage(stock_df, window=50, column='Close'):
    if isinstance(stock_df, pd.DataFrame):
        s = stock_df[column].rolling(window=window).mean()
        return s
    raise ValueError('pass a DataFrame to getMovingAverage')

def getRSI(stock_df, period=14, column='Close'):
    if isinstance(stock_df, pd.DataFrame):
        delta = stock_df[column].diff()
        up = delta.clip(lower=0)
        down = -1*delta.clip(upper=0)
        ma_up = up.ewm(com=period-1, adjust=False).mean()
        ma_down = down.ewm(com=period-1, adjust=False).mean()
        rs = ma_up/ma_down
        rsi = 100 - (100/(1+rs))
        return rsi
    raise ValueError('pass a DataFrame to getRSI')

def getMACD(stock_df, fast=12, slow=26, signal=9, column='Close'):
    if isinstance(stock_df, pd.DataFrame):
        ema_fast = stock_df[column].ewm(span=fast, adjust=False).mean()
        ema_slow = stock_df[column].ewm(span=slow, adjust=False).mean()
        macd = ema_fast - ema_slow
        sig = macd.ewm(span=signal, adjust=False).mean()
        return macd, sig
    raise ValueError('pass a DataFrame to getMACD')

def getBollingerBands(stock_df, window=20, column='Close'):
    if isinstance(stock_df, pd.DataFrame):
        mid = stock_df[column].rolling(window).mean()
        std = stock_df[column].rolling(window).std()
        upper = mid + (std*2)
        lower = mid - (std*2)
        return upper, mid, lower
    raise ValueError('pass a DataFrame to getBollingerBands')
