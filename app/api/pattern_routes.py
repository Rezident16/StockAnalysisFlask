from flask import Blueprint, jsonify
from .pattern_helpers import get_barset, patterns_result

pattern_routes = Blueprint('patterns', __name__)

# Helpers
timeframes = {
    1: '15Min',
    2: '30Min',
    3: '1Hour',
    4: '1Day',
    5: '1Week',
}

def bar_to_dict(bar):
    return {
        'close': round(bar.c, 2),
        'high': round(bar.h, 2),
        'low': round(bar.l, 2),
        'open': round(bar.o, 2),
        "date": bar.t,
    }

def get_timeframe_and_barset(id, stock):
    if id not in timeframes:
        return 'Invalid id', None

    timeframe = timeframes[id]
    barset = get_barset(stock, timeframe)  # Flask Server
    json_barset = [bar_to_dict(bar) for bar in barset]
    return timeframe, json_barset

@pattern_routes.route('/<symbol>/<int:timeFrameChosen>')
def get_patterns(symbol, timeFrameChosen):
    if timeFrameChosen not in timeframes:
        return 'Invalid id'
    timeframe, json_barset = get_timeframe_and_barset(timeFrameChosen, symbol)
    patternsResult = patterns_result(json_barset, symbol, timeframe)

    return jsonify(patternsResult)
