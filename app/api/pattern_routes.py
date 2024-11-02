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
        'time': bar.Index[1],
        'open': round(bar.open, 2),
        'high': round(bar.high, 2),
        'low': round(bar.low, 2),
        'close': round(bar.close, 2),
        'volume': bar.volume
    }

def get_timeframe_and_barset(timeFrameChosen, symbol):
    timeFrame = timeframes[timeFrameChosen]
    barset = get_barset(symbol, timeFrame)
    json_barset = [bar_to_dict(bar) for bar in barset.itertuples()]
    return timeFrameChosen, json_barset

@pattern_routes.route('/<symbol>/<int:timeFrameChosen>')
def get_patterns(symbol, timeFrameChosen):
    if timeFrameChosen not in timeframes:
        return 'Invalid id', 400
    timeframe, barset = get_timeframe_and_barset(timeFrameChosen, symbol)
    patternsResult = patterns_result(barset, symbol, timeframe)

    return jsonify(patternsResult)
