"""Helper functions used across the package."""
import re, requests, urllib.parse
from bs4 import BeautifulSoup

USER_AGENT = {'User-Agent':'Mozilla/5.0'}

def find_moneycontrol_page(stock_name):
    q = urllib.parse.quote(stock_name)
    url = f'https://www.moneycontrol.com/india/stockpricequote.php?searchtxt={q}'
    r = requests.get(url, headers=USER_AGENT, timeout=10)
    if r.ok:
        return r.url
    return None

def clean_numeric(s):
    if s is None:
        return None
    s = str(s).replace(',', '')
    s = re.sub('[^0-9.-]', '', s)
    try:
        return float(s)
    except:
        return None
