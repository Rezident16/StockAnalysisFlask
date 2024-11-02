from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
<<<<<<< HEAD
from alpaca_trade_api import REST, TimeFrame, TimeFrameUnit
=======
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest, StockSnapshotRequest
from alpaca.data.timeframe import TimeFrame
>>>>>>> 3862a56 (.)
from dotenv import load_dotenv
import talib
import numpy as np
import os
from flask import current_app

<<<<<<< HEAD


load_dotenv()
# Global Variables
=======
load_dotenv()

# Variables
>>>>>>> 3862a56 (.)
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
BASE_URL = os.getenv("BASE_URL")
ALPACA_CREDS = {
<<<<<<< HEAD
    "API_KEY":API_KEY, 
    "API_SECRET": API_SECRET, 
}
api = REST(base_url=BASE_URL, key_id=API_KEY, secret_key=API_SECRET)
=======
    "API_KEY": API_KEY, 
    "API_SECRET": API_SECRET, 
}
client = StockHistoricalDataClient(API_KEY, API_SECRET)
>>>>>>> 3862a56 (.)
DATE_FORMAT = '%Y-%m-%d'

PATTERNS = [
    "CDL2CROWS", "CDL3BLACKCROWS", "CDL3INSIDE", "CDL3LINESTRIKE", "CDL3OUTSIDE",
    "CDL3STARSINSOUTH", "CDL3WHITESOLDIERS", "CDLABANDONEDBABY", "CDLADVANCEBLOCK",
    "CDLBELTHOLD", "CDLBREAKAWAY", "CDLCLOSINGMARUBOZU", "CDLCONCEALBABYSWALL",
    "CDLCOUNTERATTACK", "CDLDARKCLOUDCOVER", "CDLDOJI", "CDLDOJISTAR", "CDLDRAGONFLYDOJI",
    "CDLENGULFING", "CDLEVENINGDOJISTAR", "CDLEVENINGSTAR", "CDLGAPSIDESIDEWHITE",
    "CDLGRAVESTONEDOJI", "CDLHAMMER", "CDLHANGINGMAN", "CDLHARAMI", "CDLHARAMICROSS",
    "CDLHIGHWAVE", "CDLHIKKAKE", "CDLHIKKAKEMOD", "CDLHOMINGPIGEON", "CDLIDENTICAL3CROWS",
    "CDLINNECK", "CDLINVERTEDHAMMER", "CDLKICKING", "CDLKICKINGBYLENGTH", "CDLLADDERBOTTOM",
    "CDLLONGLEGGEDDOJI", "CDLLONGLINE", "CDLMARUBOZU", "CDLMATCHINGLOW", "CDLMATHOLD",
    "CDLMORNINGDOJISTAR", "CDLMORNINGSTAR", "CDLONNECK", "CDLPIERCING", "CDLRICKSHAWMAN",
    "CDLRISEFALL3METHODS", "CDLSEPARATINGLINES", "CDLSHOOTINGSTAR", "CDLSHORTLINE",
    "CDLSPINNINGTOP", "CDLSTALLEDPATTERN", "CDLSTICKSANDWICH", "CDLTAKURI", "CDLTASUKIGAP",
    "CDLTHRUSTING", "CDLTRISTAR", "CDLUNIQUE3RIVER", "CDLUPSIDEGAP2CROWS", "CDLXSIDEGAP3METHODS"
]

def get_barset(stock, timeFrameChosen):
    # Stock is a symbol
    _, _, one_month_ago, _, _, year_ago, five_year_ago = get_dates()
    if timeFrameChosen == '15Min':
<<<<<<< HEAD
        barset = api.get_bars(stock,timeframe=TimeFrame(15, TimeFrameUnit.Minute), limit=100) # 15 Min timeframe
    elif timeFrameChosen == '30Min':
        barset = api.get_bars(stock,timeframe=TimeFrame(30, TimeFrameUnit.Minute), limit=50) # 30 Min timeframe
    elif timeFrameChosen == '1Hour':
        barset = api.get_bars(stock,timeframe=TimeFrame.Hour, start = one_month_ago, limit=750) # Hourly timeframe
    elif timeFrameChosen == '1Day':
        barset = api.get_bars(stock, TimeFrame.Day, start = year_ago , limit=367) # Daily timeframe
    else:
        barset = api.get_bars(stock, TimeFrame.Week, start = five_year_ago, limit=264) # Weekly timeframe
=======
        request_params = StockBarsRequest(
            symbol_or_symbols=stock,
            timeframe=TimeFrame.Minute,
            start=one_month_ago,
            limit=100
        )
    elif timeFrameChosen == '30Min':
        request_params = StockBarsRequest(
            symbol_or_symbols=stock,
            timeframe=TimeFrame.Minute,
            start=one_month_ago,
            limit=50
        )
    elif timeFrameChosen == '1Hour':
        request_params = StockBarsRequest(
            symbol_or_symbols=stock,
            timeframe=TimeFrame.Hour,
            start=one_month_ago,
            limit=750
        )
    elif timeFrameChosen == '1Day':
        request_params = StockBarsRequest(
            symbol_or_symbols=stock,
            timeframe=TimeFrame.Day,
            start=year_ago,
            limit=367
        )
    else:
        request_params = StockBarsRequest(
            symbol_or_symbols=stock,
            timeframe=TimeFrame.Week,
            start=five_year_ago,
            limit=264
        )
    barset = client.get_stock_bars(request_params).df
>>>>>>> 3862a56 (.)
    return barset

def patterns_result(barset, stock, timeframe):
    open, high, low, close, date = extract_data(barset)
    results = {}

    for pattern in PATTERNS:
        result_list = check_pattern(pattern, open, high, low, close)
        bullish_bearish_result = create_results(result_list, date, pattern, stock, timeframe, close)
        if len(bullish_bearish_result) > 0:
            results[pattern] = bullish_bearish_result

    return results

def get_price(stock):
<<<<<<< HEAD
    snapshot = api.get_snapshot(stock)
    return snapshot.minute_bar.vw
=======
    request_params = StockSnapshotRequest(symbol_or_symbols=stock)
    snapshot = client.get_stock_snapshot(request_params)
    return snapshot[stock].minute_bar.vw
>>>>>>> 3862a56 (.)

def check_pattern(pattern, open, high, low, close):
    function = getattr(talib, pattern)
    result = function(open, high, low, close)
    return result.tolist()

def create_results(result_list, date, pattern, stock, timeframe, close):
    return [
<<<<<<< HEAD
        {"date": date[i],"milliseconds": convert_date_to_milliseconds(date[i]), "value": value, "sentiment": 'Bullish', "pattern": pattern, "stock": stock, 'timeframe': timeframe, 'close': close[i] } if value >= 100 
        else {"date":date[i],"milliseconds": convert_date_to_milliseconds(date[i]), "value": value, "sentiment": 'Bearish', "pattern": pattern, "stock": stock,'timeframe': timeframe, 'close': close[i]} 
=======
        {"date": date[i], "milliseconds": convert_date_to_milliseconds(date[i]), "value": value, "sentiment": 'Bullish', "pattern": pattern, "stock": stock, 'timeframe': timeframe, 'close': close[i]} if value >= 100 
        else {"date": date[i], "milliseconds": convert_date_to_milliseconds(date[i]), "value": value, "sentiment": 'Bearish', "pattern": pattern, "stock": stock, 'timeframe': timeframe, 'close': close[i]} 
>>>>>>> 3862a56 (.)
        for i, value in enumerate(result_list) if value >= 100 or value <= -100
    ]

def convert_date_to_milliseconds(date_timestamp):
    return int(date_timestamp.to_pydatetime().timestamp() * 1000)

def get_dates(): 
    today = datetime.now().date() - timedelta(days=1)
    one_week_ago = today - timedelta(weeks=1)
    one_month_ago = today - relativedelta(months=1)
    three_month_ago = today - relativedelta(months=3)
    start_of_year = datetime(today.year, 1, 1).date()
    year_ago = today - relativedelta(years=1)
    five_year_ago = today - relativedelta(years=5)
    return today.strftime(DATE_FORMAT), one_week_ago.strftime(DATE_FORMAT), one_month_ago.strftime(DATE_FORMAT), three_month_ago.strftime(DATE_FORMAT), start_of_year.strftime(DATE_FORMAT), year_ago.strftime(DATE_FORMAT), five_year_ago.strftime(DATE_FORMAT)

def extract_data(barset):
    open = np.array([bar['open'] for bar in barset]).astype('double')
    high = np.array([bar['high'] for bar in barset]).astype('double')
    low = np.array([bar['low'] for bar in barset]).astype('double')
    close = np.array([bar['close'] for bar in barset]).astype('double')
<<<<<<< HEAD
    date = np.array([bar['date'] for bar in barset])
=======
    date = np.array([bar['time'] for bar in barset])
>>>>>>> 3862a56 (.)
    return open, high, low, close, date
