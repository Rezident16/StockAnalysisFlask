from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest, StockSnapshotRequest
from alpaca.data.timeframe import TimeFrame
from dotenv import load_dotenv
import talib
import numpy as np
import os
from flask import current_app

load_dotenv()

# Variables
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
BASE_URL = os.getenv("BASE_URL")
ALPACA_CREDS = {
    "API_KEY": API_KEY, 
    "API_SECRET": API_SECRET, 
}
client = StockHistoricalDataClient(API_KEY, API_SECRET)
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
    request_params = StockSnapshotRequest(symbol_or_symbols=stock)
    snapshot = client.get_stock_snapshot(request_params)
    return snapshot[stock].minute_bar.vw

def check_pattern(pattern, open, high, low, close):
    function = getattr(talib, pattern)
    result = function(open, high, low, close)
    return result.tolist()

def create_results(result_list, date, pattern, stock, timeframe, close):
    return [
        {"date": date[i], "milliseconds": convert_date_to_milliseconds(date[i]), "value": value, "sentiment": 'Bullish', "pattern": pattern, "stock": stock, 'timeframe': timeframe, 'close': close[i]} if value >= 100 
        else {"date": date[i], "milliseconds": convert_date_to_milliseconds(date[i]), "value": value, "sentiment": 'Bearish', "pattern": pattern, "stock": stock, 'timeframe': timeframe, 'close': close[i]} 
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
    date = np.array([bar['time'] for bar in barset])
    return open, high, low, close, date
