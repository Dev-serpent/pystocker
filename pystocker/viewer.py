"""Simple plotting utilities using matplotlib. The viewer functions accept a DataFrame or stock name (which will be fetched)."
"""
import matplotlib.pyplot as plt
import pandas as pd
from .core import getAllData

def plotStock(stock_or_df, columns=['Close']):
    if isinstance(stock_or_df, pd.DataFrame):
        df = stock_or_df.copy()
    else:
        df = getAllData(stock_or_df)
    if 'Date' in df.columns:
        df = df.set_index('Date')
    ax = df[columns].plot(title='Stock Plot', figsize=(10,6))
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    plt.grid(True)
    plt.show()

def plotVolume(stock_or_df):
    if isinstance(stock_or_df, pd.DataFrame):
        df = stock_or_df.copy()
    else:
        df = getAllData(stock_or_df)
    if 'Date' in df.columns:
        df = df.set_index('Date')
    ax = df['Volume'].plot(title='Volume', figsize=(10,4))
    ax.set_xlabel('Date')
    plt.show()

def candlestickChart(stock_or_df):
    try:
        import mplfinance as mpf
    except Exception:
        raise RuntimeError('mplfinance required for candlestick charts (pip install mplfinance)')
    if isinstance(stock_or_df, pd.DataFrame):
        df = stock_or_df.copy()
    else:
        df = getAllData(stock_or_df)
    if 'Date' in df.columns:
        df = df.set_index('Date')
    mpf.plot(df[['Open','High','Low','Close']], type='candle', style='charles')
