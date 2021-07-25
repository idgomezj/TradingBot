import requests
import json
from .config import *
from pandas import DataFrame
from datetime import datetime
import alpaca_trade_api as tradeapi


api = tradeapi.REST(
    key_id=API_KEY,
    secret_key=SECRET_KEY,
    base_url=ENDPOINT_URL
)


def get_bar(symbol, start, end, time, limit=4):
    asset = api.get_asset(symbol)
    if asset.tradable:
        bar = api.get_barset(symbol, time, start=start,
                             end=end, limit=limit).df

    return(bar)


def get_list():
    active_assets = api.list_assets(status='active')
    active_assets = [a for a in active_assets if a.exchange == 'NASDAQ']
    short_list = []
    for asset in active_assets:
        if asset.easy_to_borrow and asset.marginable:
            short_list.append(asset.symbol)
    return short_list


def get_info():
    account = api.get_account()
    portfolio = api.list_positions()
    return [account, portfolio]


def get_account():
    r = requests.get(ACCOUNT_URL, headers=HEADERS)
    return json.loads(r.content)


def order_buy(symbol, qty, type1='market', time_in_force='gtc', side='buy'):
    r = api.submit_order(symbol=symbol, qty=qty, side=side,
                         type=type1, time_in_force=time_in_force)
    print('Already Buy')
    return r


def order_sell(symbol, qty, type1='market', time_in_force='gtc', side='sell'):
    r = api.submit_order(symbol=symbol, qty=qty, side=side,
                         type=type1, time_in_force=time_in_force)
    print('Already Sell')
    return r


def order_stop_lost(symbol, qty, percent=1.0):
    r = api.submit_order(
        symbol=symbol,
        qty=qty,
        side='sell',
        type='trailing_stop',
        trail_percent=percent,  # stop price will be hwm*0.99
        time_in_force='gtc',
    )
    print('Already Stop Lost')
    return r


def cancel_alpaca_orders():
    r = api.cancel_all_orders()
    return r
