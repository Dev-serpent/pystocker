import pandas as pd
from .functions import getAllData

def getDod(date, symbol):
    df = getAllData(symbol)
    if df.empty or 'Date' not in df.columns or 'Close' not in df.columns:
        return None
    df = df.sort_values('Date').reset_index(drop=True)
    d = pd.to_datetime(date).date()
    idx = df.index[df['Date'] == d]
    if len(idx)==0: return None
    i = idx[0]
    if i==0: return 0.0
    prev = df.loc[i-1,'Close']
    curr = df.loc[i,'Close']
    if prev in (0,None): return None
    return ((curr - prev)/prev)*100

def getChangeSeries(symbol):
    df = getAllData(symbol)
    if df.empty or 'Close' not in df.columns:
        return pd.Series(dtype=float)
    return df['Close'].pct_change().fillna(0)*100

def getYTD(symbol):
    df = getAllData(symbol)
    if df.empty or 'Date' not in df.columns or 'Close' not in df.columns:
        return None
    df = df.sort_values('Date').reset_index(drop=True)
    this_year = pd.Timestamp.now().year
    start = pd.Timestamp(year=this_year, month=1, day=1).date()
    df_y = df[df['Date']>=start]
    if df_y.empty: return None
    start_price = df_y.iloc[0]['Close']
    end_price = df_y.iloc[-1]['Close']
    return ((end_price - start_price)/start_price)*100

def getCAGR(symbol, years=5):
    df = getAllData(symbol)
    if df.empty or 'Close' not in df.columns: return None
    df = df.sort_values('Date').reset_index(drop=True)
    if df.empty: return None
    end_price = df['Close'].iloc[-1]
    start_idx = max(0, len(df)-1 - int(years*252))
    start_price = df['Close'].iloc[start_idx]
    if start_price in (None,0): return None
    periods = (df['Date'].iloc[-1] - df['Date'].iloc[start_idx]).days/365.25
    return ((end_price/start_price)**(1/periods)-1)*100
