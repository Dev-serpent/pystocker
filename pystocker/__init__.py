"""pystocker - expanded stock data library (Moneycontrol API + helpers)

Exports high-level functions:
- getAllData, getLatest, getRange, getMetadata, getOpen, getHigh, getLow,
  getClose, getPrevClose, getVolume
- getDod, getChangeSeries, getYTD, getCAGR
- getMovingAverage, getRSI, getMACD, getBollingerBands
- compareStocks, correlateStocks
- plotStock, plotVolume, candlestickChart
"""

from .functions import (
    getAllData, getLatest, getRange, getMetadata,
    getOpen, getHigh, getLow, getClose, getPrevClose, getVolume
)
from .analyzer import getDod, getChangeSeries, getYTD, getCAGR
from .technicals import getMovingAverage, getRSI, getMACD, getBollingerBands
from .compare import compareStocks, correlateStocks
from .viewer import plotStock, plotVolume, candlestickChart

__all__ = [
    'getAllData','getLatest','getRange','getMetadata',
    'getOpen','getHigh','getLow','getClose','getPrevClose','getVolume',
    'getDod','getChangeSeries','getYTD','getCAGR',
    'getMovingAverage','getRSI','getMACD','getBollingerBands',
    'compareStocks','correlateStocks',
    'plotStock','plotVolume','candlestickChart'
]
