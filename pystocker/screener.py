"""Simple screeners - best-effort using Moneycontrol pages and market snapshots."""
import requests
from bs4 import BeautifulSoup

USER_AGENT = {'User-Agent': 'Mozilla/5.0'}

def searchStocks(query):
    try:
        q = query.replace(' ', '+')
        url = f'https://www.moneycontrol.com/india/stockpricequote.php?searchtxt={q}'
        r = requests.get(url, headers=USER_AGENT, timeout=10)
        return r.url
    except:
        return None

def getTopGainers():
    return []

def getTopLosers():
    return []

def getMostActive():
    return []
