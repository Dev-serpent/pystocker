"""Core data fetch functions for pystocker.

These functions fetch stock data (historical tables and metadata) from Moneycontrol.
They are intentionally defensive (exceptions handled) and return pandas DataFrames / primitives.
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import re
import urllib.parse
import time

USER_AGENT = {'User-Agent': 'Mozilla/5.0'}

def _moneycontrol_search(stock_name):
    """Search Moneycontrol for a stock symbol/page. Returns the first search-result URL (best-effort)."""
    q = urllib.parse.quote(stock_name)
    url = f'https://www.moneycontrol.com/india/stockpricequote.php?searchtxt={q}'
    try:
        r = requests.get(url, headers=USER_AGENT, timeout=10)
        r.raise_for_status()
        return r.url
    except Exception:
        return None

def _parse_historical_table(soup):
    """Try to extract historical data table from a Moneycontrol-like page."""
    tables = soup.find_all('table')
    candidate = None
    for t in tables:
        headers = [th.get_text(strip=True).lower() for th in t.find_all('th')]
        if any('date' in h for h in headers) and any('close' in h for h in headers):
            candidate = t
            break
    if candidate is None:
        for t in tables:
            rows = t.find_all('tr')
            if len(rows) > 3:
                candidate = t
                break
    if candidate is None:
        return pd.DataFrame()

    rows = candidate.find_all('tr')
    data = []
    header = [th.get_text(strip=True) for th in candidate.find_all('th')]
    for r in rows:
        cells = r.find_all(['td','th'])
        if not cells:
            continue
        values = [c.get_text(strip=True) for c in cells]
        if header and values == header:
            continue
        if len(values) >= 2:
            data.append(values)
    df = pd.DataFrame(data)
    if header and df.shape[1] == len(header):
        df.columns = header
    else:
        possible = ['Date','Open','High','Low','Close','Volume','Change','%Change','Prev Close']
        n = min(len(possible), df.shape[1])
        df.columns = possible[:n] + [f'col{i}' for i in range(n, df.shape[1])]
    return df

def _clean_numeric(s):
    if s is None:
        return None
    s = str(s).replace(',', '').strip()
    s = re.sub(r'[^0-9.-]', '', s)
    if s == '':
        return None
    try:
        return float(s)
    except:
        return None

def getAllData(stock):
    """Return a pandas DataFrame with historical stock data for `stock` (name or ticker)."""
    url = _moneycontrol_search(stock)
    if not url:
        raise ValueError(f"Could not locate Moneycontrol page for '{stock}'")
    r = requests.get(url, headers=USER_AGENT, timeout=10)
    soup = BeautifulSoup(r.text, 'html.parser')
    df = _parse_historical_table(soup)
    for c in df.columns:
        lc = c.lower()
        if 'date' in lc:
            try:
                df[c] = pd.to_datetime(df[c], errors='coerce', dayfirst=True)
            except:
                df[c] = df[c]
        else:
            df[c] = df[c].apply(_clean_numeric)
    rename_map = {}
    for c in df.columns:
        if 'close' in c.lower():
            rename_map[c] = 'Close'
        elif 'open' in c.lower():
            rename_map[c] = 'Open'
        elif 'high' in c.lower():
            rename_map[c] = 'High'
        elif 'low' in c.lower():
            rename_map[c] = 'Low'
        elif 'volume' in c.lower():
            rename_map[c] = 'Volume'
        elif 'date' in c.lower():
            rename_map[c] = 'Date'
    df = df.rename(columns=rename_map)
    if 'Date' in df.columns:
        df = df.sort_values('Date').reset_index(drop=True)
    return df

def getLatest(stock):
    """Return a dictionary snapshot (Open, High, Low, Close, Volume) from the stock page's summary block."""
    url = _moneycontrol_search(stock)
    if not url:
        return {}
    r = requests.get(url, headers=USER_AGENT, timeout=10)
    soup = BeautifulSoup(r.text, 'html.parser')
    out = {}
    for lbl in ['Open','Prev Close','Close','High','Low','Volume','Market Cap','P/E']:
        el = soup.find(text=re.compile(lbl, re.I))
        if el:
            parent = el.parent
            sval = None
            sib = parent.find_next_sibling()
            if sib:
                sval = sib.get_text(strip=True)
            if not sval:
                sval = parent.parent.get_text(separator=' ', strip=True)
            out[lbl] = sval
    return out

def getRange(stock, start_date, end_date):
    df = getAllData(stock)
    if 'Date' not in df.columns:
        return pd.DataFrame()
    s = pd.to_datetime(start_date)
    e = pd.to_datetime(end_date)
    return df[(df['Date'] >= s) & (df['Date'] <= e)].reset_index(drop=True)

def getOpen(date, stock):
    df = getAllData(stock)
    if 'Date' not in df.columns or 'Open' not in df.columns:
        return None
    row = df[df['Date'] == pd.to_datetime(date)]
    if row.empty:
        return None
    return float(row['Open'].iloc[0])

def getHigh(date, stock):
    df = getAllData(stock)
    if 'Date' not in df.columns or 'High' not in df.columns:
        return None
    row = df[df['Date'] == pd.to_datetime(date)]
    if row.empty:
        return None
    return float(row['High'].iloc[0])

def getLow(date, stock):
    df = getAllData(stock)
    if 'Date' not in df.columns or 'Low' not in df.columns:
        return None
    row = df[df['Date'] == pd.to_datetime(date)]
    if row.empty:
        return None
    return float(row['Low'].iloc[0])

def getClose(date, stock):
    df = getAllData(stock)
    if 'Date' not in df.columns or 'Close' not in df.columns:
        return None
    row = df[df['Date'] == pd.to_datetime(date)]
    if row.empty:
        return None
    return float(row['Close'].iloc[0])

def getPrevClose(date, stock):
    df = getAllData(stock)
    if 'Date' not in df.columns or 'Close' not in df.columns:
        return None
    d = pd.to_datetime(date)
    df = df.sort_values('Date').reset_index(drop=True)
    idx = df.index[df['Date'] == d]
    if len(idx)==0:
        return None
    i = idx[0]
    if i==0:
        return None
    return float(df.loc[i-1,'Close'])
