from Alpaca import *
import talib
import yfinance as yf
import time
import pandas as pd
import datetime as dt
from IexCloud import *
from .Reversal_Patterns import reversal_patterns, pattern_down,pattern_up
from Mongo import *


def watch_sell(id_process, percent):
    print('\x1b[6;32;40m' + 'Activate Wath_Sell Process' + '\x1b[0m')
    watch = True
    value = 0
    cycle = True
    do_other_cycle = True
    account, posittion = get_info()
    if posittion:
        symbol = posittion[0].symbol
        qty = posittion[0].qty
    else:
        cycle = False
        do_other_cycle = False

    while cycle:
        time.sleep(2)
        account, posittion = get_info()
        if posittion:
            if float(posittion[0].unrealized_intraday_plpc) > 0.002:
                cycle_stop_lost = True
                while cycle_stop_lost:
                    try:
                        account, posittion = get_info()
                        gap = float(posittion[0].unrealized_pl) / \
                            float(posittion[0].avg_entry_price)
                        if percent > gap:
                            if gap/2 < 0.1:
                                percent = 0.1
                            else:
                                percent = gap/2
                        else:
                            percent = percent / 2
                            if percent < 0.1:
                                percent = 0.1
                        cancel_alpaca_orders()
                        stop_lost_order = order_stop_lost(
                            symbol=symbol, qty=qty, percent=percent)
                        cycle = False
                        cycle_stop_lost = False
                    except:
                        if posittion:
                            time.sleep(3)
                        else:
                            cycle = False
                            cycle_stop_lost = False
                            do_other_cycle = False
                cycle = False
        else:
            cycle = False
            do_other_cycle = False

    if do_other_cycle:
        while watch:
            account, posittion = get_info()
            if posittion:
                if paterns(symbol, condition_reversal_patterns=True,condition_pattern_down=True,condition_pattern_up=False) < -200:
                    cancel_alpaca_orders()
                    order = order_sell(symbol, qty, type1='market',
                                       time_in_force='gtc', side='sell')
                    Buy_Mongo_update(value, id_process)
                    watch = False
                    time.sleep(5)
                else:
                    time.sleep(5)
            else:
                Buy_Mongo_update(value, id_process)
                order = []
                watch = False
    else:
        order = []
        Buy_Mongo_update(value, id_process)
    return order


def paterns(symbol, condition_reversal_patterns:True,condition_pattern_down:True,condition_pattern_up:True):
    today = (dt.datetime.today()+dt.timedelta(1)).strftime('%Y-%m-%d')
    hist = (dt.datetime.today()-dt.timedelta(3)).strftime('%Y-%m-%d')
    vector = [1, 2, 3, 4, 5]
    suma = 0
    cycle = True
    while cycle:
        try:
            df = yf.download(symbol, interval='5m', start=hist,
                             end=today, threads=False, progress=False)
            cycle = False
        except Exception as e:
            print(e)
            time.sleep(5)
            continue
    df = df.rename(columns={"Open": "open", "High": "high",
                                    "Low": "low", "Close": "close", "Volume": "volume"})
    if condition_reversal_patterns:
        for pattern in reversal_patterns:
            pattern_function = getattr(talib, pattern)
            #print(df)
            df[reversal_patterns[pattern]] = pattern_function(
                df['open'], df['high'], df['low'], df['close'])
            suma += df[reversal_patterns[pattern]][-5:]*vector
    if condition_pattern_down:
        for pattern in pattern_down:
            pattern_function = getattr(talib, pattern)
            df[pattern_down[pattern]] = pattern_function(
                df['open'], df['high'], df['low'], df['close'])
            suma += df[pattern_down[pattern]][-5:]*vector
    if condition_pattern_up:    
        for pattern in pattern_up:
            pattern_function = getattr(talib, pattern)
            df[pattern_up[pattern]] = pattern_function(
                df['open'], df['high'], df['low'], df['close'])
            suma += df[pattern_up[pattern]][-5:]*vector
    print('\x1b[6;36;40m' + "Ready Paterns" + '\x1b[0m')
    result = suma.sum()
    #print('The patern is {}'.format(result))
    return result
