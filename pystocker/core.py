"""Core network functions: talk to Moneycontrol's JSON endpoints (priceapi) and fallback HTML parsing."""
import requests, time, datetime, urllib.parse
import re
from bs4 import BeautifulSoup

USER_AGENT = {'User-Agent': 'Mozilla/5.0'}

PRICEAPI_HISTORY = 'https://priceapi.moneycontrol.com/techCharts/indianMarket/stock/history'
AUTOSUGGEST = 'https://www.moneycontrol.com/mccode/common/autosuggesion.php'

def _autosuggest(name):
    """Return first autosuggest result dict or None."""
    try:
        params = {'query': name, 'type': 1, 'format':'json'}
        r = requests.get(AUTOSUGGEST, params=params, headers=USER_AGENT, timeout=10)
        r.raise_for_status()
        j = r.json()
        if isinstance(j, list) and len(j)>0:
            return j[0]
    except Exception:
        return None
    return None

def normalize_symbol(symbol_or_name):
    """Try to return a symbol usable by the price API. Accepts either a known symbol or company name."""
    if not symbol_or_name:
        return None
    s = str(symbol_or_name).strip()
    # if it looks like an uppercase ticker, return as-is
    if s.isupper() and len(s) <= 20 and ' ' not in s:
        return s
    # try autosuggest to find symbol or link_src
    res = _autosuggest(s)
    if not res:
        return s.replace(' ', '').upper()
    # res may contain 'symbol' or 'scrip_code' or 'link_src'
    if 'symbol' in res:
        return res['symbol']
    if 'scrip_code' in res:
        return str(res['scrip_code'])
    if 'link_src' in res:
        # attempt to extract trailing segment as symbol-like text
        seg = res['link_src'].rstrip('/').split('/')[-1]
        return seg.upper()
    # fallback
    return s.replace(' ', '').upper()

def fetch_stock_history(symbol, start=None, end=None, resolution='1D'):
    """Fetch OHLCV history via priceapi.moneycontrol.com.

    symbol may be a symbol code or a company name (we try to normalize).
    Returns a dict with arrays or raises requests.HTTPError on failure.
    """
    sym = normalize_symbol(symbol)
    now = int(time.time())
    if end is None:
        end = now
    if start is None:
        # default: last 365 days
        start = now - 365*24*3600
    params = {'symbol': sym, 'resolution': resolution, 'from': int(start), 'to': int(end)}
    r = requests.get(PRICEAPI_HISTORY, params=params, headers=USER_AGENT, timeout=15)
    r.raise_for_status()
    return r.json()

def fetch_moneycontrol_page(symbol_or_name):
    """Return Moneycontrol page HTML (first autosuggest link or built search)."""
    res = _autosuggest(symbol_or_name)
    if res and 'link_src' in res:
        url = urllib.parse.urljoin('https://www.moneycontrol.com', res['link_src'])
    else:
        # fallback to search page
        q = urllib.parse.quote(symbol_or_name)
        url = f'https://www.moneycontrol.com/india/stockpricequote.php?searchtxt={q}'
    r = requests.get(url, headers=USER_AGENT, timeout=15)
    r.raise_for_status()
    return r.text

def parse_snapshot_from_html(html_text):
    """Best-effort parse snapshot metadata from Moneycontrol HTML."""
    soup = BeautifulSoup(html_text, 'html.parser')
    meta = {}
    # common labels
    labels = ['Open', 'Prev Close', 'Close', 'High', 'Low', 'Volume', 'Market Cap', 'P/E', '52 Week High', '52 Week Low', 'Face Value', 'Dividend Yield']
    text = soup.get_text(separator='\n')
    for lbl in labels:
        m = re.search(rf"{re.escape(lbl)}[:\s]*([^\n]+)", text, flags=re.I)
        if m:
            meta[lbl] = m.group(1).strip()
    # fallback: look for label nodes
    for lbl in labels:
        el = soup.find(text=re.compile(rf'^{lbl}$', re.I))
        if el:
            sib = el.parent.find_next_sibling()
            if sib:
                meta[lbl] = sib.get_text(strip=True)
    return meta
