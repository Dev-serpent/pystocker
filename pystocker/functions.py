"""High-level wrappers returning pandas-friendly structures."""
from .core import fetch_stock_history, fetch_moneycontrol_page, parse_snapshot_from_html, normalize_symbol
import pandas as pd
import datetime

def getAllData(symbol, start=None, end=None, resolution='1D'):
    """Return pandas.DataFrame with Date, Open, High, Low, Close, Volume columns (if available)."""
    j = fetch_stock_history(symbol, start=start, end=end, resolution=resolution)
    # expect keys 't','o','h','l','c','v'
    if not j or 't' not in j:
        return pd.DataFrame()
    rows = []
    for i in range(len(j['t'])):
        rows.append({
            'Date': datetime.datetime.fromtimestamp(j['t'][i]).date(),
            'Open': j.get('o',[None])[i] if 'o' in j else None,
            'High': j.get('h',[None])[i] if 'h' in j else None,
            'Low': j.get('l',[None])[i] if 'l' in j else None,
            'Close': j.get('c',[None])[i] if 'c' in j else None,
            'Volume': j.get('v',[None])[i] if 'v' in j else None
        })
    df = pd.DataFrame(rows)
    df = df.dropna(subset=['Date']).reset_index(drop=True)
    return df

def getLatest(symbol):
    df = getAllData(symbol)
    if df.empty:
        return {}
    last = df.iloc[-1].to_dict()
    last['Date'] = str(last['Date'])
    return last

def getRange(symbol, start_date, end_date):
    df = getAllData(symbol)
    if df.empty or 'Date' not in df.columns:
        return pd.DataFrame()
    s = pd.to_datetime(start_date).date()
    e = pd.to_datetime(end_date).date()
    return df[(df['Date'] >= s) & (df['Date'] <= e)].reset_index(drop=True)

def getOpen(date, symbol):
    df = getAllData(symbol)
    if df.empty: return None
    row = df[df['Date'] == pd.to_datetime(date).date()]
    if row.empty: return None
    return float(row.iloc[0]['Open']) if not pd.isna(row.iloc[0]['Open']) else None

def getHigh(date, symbol):
    df = getAllData(symbol)
    if df.empty: return None
    row = df[df['Date'] == pd.to_datetime(date).date()]
    if row.empty: return None
    return float(row.iloc[0]['High']) if not pd.isna(row.iloc[0]['High']) else None

def getLow(date, symbol):
    df = getAllData(symbol)
    if df.empty: return None
    row = df[df['Date'] == pd.to_datetime(date).date()]
    if row.empty: return None
    return float(row.iloc[0]['Low']) if not pd.isna(row.iloc[0]['Low']) else None

def getClose(date, symbol):
    df = getAllData(symbol)
    if df.empty: return None
    row = df[df['Date'] == pd.to_datetime(date).date()]
    if row.empty: return None
    return float(row.iloc[0]['Close']) if not pd.isna(row.iloc[0]['Close']) else None

def getPrevClose(date, symbol):
    df = getAllData(symbol)
    if df.empty or 'Date' not in df.columns: return None
    df = df.sort_values('Date').reset_index(drop=True)
    d = pd.to_datetime(date).date()
    idx = df.index[df['Date'] == d]
    if len(idx)==0: return None
    i = idx[0]
    if i==0: return None
    return float(df.loc[i-1,'Close']) if not pd.isna(df.loc[i-1,'Close']) else None

def getVolume(date, symbol):
    df = getAllData(symbol)
    if df.empty: return None
    row = df[df['Date'] == pd.to_datetime(date).date()]
    if row.empty: return None
    return float(row.iloc[0]['Volume']) if not pd.isna(row.iloc[0]['Volume']) else None

def getMetadata(symbol_or_name):
    """Try API fallback and HTML parse to get metadata like Market Cap, P/E, etc."""
    try:
        html = fetch_moneycontrol_page(symbol_or_name)
        meta = parse_snapshot_from_html(html)
        return meta
    except:
        return {}
