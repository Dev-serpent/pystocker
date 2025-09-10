"""pystocker - lightweight stock data fetcher & analyzer

Usage:
    import pystocker as ps
    df = ps.getAllData('RELIANCE')
"""

from .core import getAllData, getLatest, getRange, getMetadata, getOpen, getHigh, getLow, getClose, getPrevClose, getVolume
from .analyzer import getDod, getChangeSeries, getYTD, getCAGR
from .technicals import getMovingAverage, getRSI, getMACD, getBollingerBands
from .compare import compareStocks, correlateStocks
from .screener import getTopGainers, getTopLosers, getMostActive, searchStocks
from .viewer import plotStock, plotVolume, candlestickChart

__all__ = [
    'getAllData','getLatest','getRange','getMetadata','getOpen','getHigh','getLow','getClose','getPrevClose','getVolume',
    'getDod','getChangeSeries','getYTD','getCAGR',
    'getMovingAverage','getRSI','getMACD','getBollingerBands',
    'compareStocks','correlateStocks',
    'getTopGainers','getTopLosers','getMostActive','searchStocks',
    'plotStock','plotVolume','candlestickChart'
]
