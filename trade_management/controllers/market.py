import time
from datetime import datetime

import yfinance as yf

_CACHE = {}
_CACHE_TTL = 900  # 15 minutes

_KC_MONTHS = [3, 5, 7, 9, 12]
_KC_CODES = {3: 'H', 5: 'K', 7: 'N', 9: 'U', 12: 'Z'}


def _next_kc_contracts(n=3):
    today = datetime.today()
    contracts = []
    year = today.year
    while len(contracts) < n:
        for m in _KC_MONTHS:
            if year == today.year and m < today.month:
                continue
            if year == today.year and m == today.month and today.day > 15:
                continue
            code = _KC_CODES[m]
            ticker = f"KC{code}{str(year)[-2:]}.NYB"
            label = datetime(year, m, 1).strftime('%b/%y')
            contracts.append({'ticker': ticker, 'label': label})
            if len(contracts) >= n:
                break
        year += 1
    return contracts


def _fetch_price(ticker_symbol):
    try:
        t = yf.Ticker(ticker_symbol)
        info = t.fast_info
        price = info.last_price
        prev = info.previous_close
        if price is None:
            return None, None, None
        change = round(price - prev, 2) if prev else None
        change_pct = round((price - prev) / prev * 100, 2) if prev else None
        return round(price, 2), change, change_pct
    except Exception:
        return None, None, None


def get_market_data():
    now = time.time()
    if 'data' in _CACHE and now - _CACHE.get('ts', 0) < _CACHE_TTL:
        return _CACHE['data']

    data = {
        'kc': [],
        'usd_brl': None,
        'usd_brl_change': None,
        'usd_brl_change_pct': None,
        'updated_at': datetime.now().strftime('%H:%M'),
    }

    price, change, pct = _fetch_price('USDBRL=X')
    data['usd_brl'] = price
    data['usd_brl_change'] = change
    data['usd_brl_change_pct'] = pct

    for c in _next_kc_contracts(3):
        price, change, pct = _fetch_price(c['ticker'])
        data['kc'].append({
            'label': c['label'],
            'price': price,
            'change': change,
            'change_pct': pct,
        })

    _CACHE['data'] = data
    _CACHE['ts'] = now
    return data
