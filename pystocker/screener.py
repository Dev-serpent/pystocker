"""Lightweight screeners (best-effort, may be extended)."""
import requests
from bs4 import BeautifulSoup

USER_AGENT = {'User-Agent': 'Mozilla/5.0'}

def searchStocks(query):
    q = query.replace(' ', '+')
    url = f'https://www.moneycontrol.com/india/stockpricequote.php?searchtxt={q}'
    try:
        r = requests.get(url, headers=USER_AGENT, timeout=10)
        return r.url
    except:
        return None

def getTopGainers():
    # Placeholder — site-specific API needed
    return []

def getTopLosers():
    return []

def getMostActive():
    return []
