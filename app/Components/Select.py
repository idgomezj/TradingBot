from Alpaca import *
import talib
import yfinance as yf
import time
import pandas as pd
import datetime as dt
from IexCloud import *
from Mongo import *
from Components import *
from TDA import *
from Components.Sell import paterns


def pre_select():
    print('\x1b[6;30;42m' + '*********** Start Pre_Select *******************' + '\x1b[0m')
    lista = []
    df = pd.read_csv('./Data/Good_List.csv')
    symbols = list(df['symbol'])
    review = []
    constant_band = 1.3
    market_cap = 20e+6
    r = {'upperband': [], 'middleband': [], 'lowerband': [],
         'macd': [], 'macdsignal': [], 'macdhist': [], 'rsi': [], 'sma10': [], 'sma40': [], 'stock': [], 'close': []}
    resultado = pd.DataFrame(data=r)
    today = (dt.datetime.today()+dt.timedelta(1)).strftime('%Y-%m-%d')
    hist = (dt.datetime.today()-dt.timedelta(20)).strftime('%Y-%m-%d')
    # symbols = ['CCL']
    c = 0
    for symbol in symbols[:]:
        c += 1

        try:
            df = yf.download(symbol, interval='1h', start=hist,
                             end=today, threads=False, progress=False)
        
        except Exception as e:
            print('.... Download Data Error')
            #print(e)
            time.sleep(5)
            continue
        df = df.rename(columns={"Open": "open", "High": "high",
                                "Low": "low", "Close": "close", "Volume": "volume"})
        a = df['volume'][-10:]*df['close'][-10:]
        
        try:
            if a.mean() > market_cap:
                df['upperband'], df['middleband'], df['lowerband'] = talib.BBANDS(df['close'],
                                                                                  timeperiod=20, nbdevup=2,
                                                                                  nbdevdn=2, matype=0)
                if df['close'][-1]/df['lowerband'][-1] < constant_band:
                    b = df[df['close'] == df['open']]
                    if len(b)/len(df) < 0.1:
                        lista.append(symbol)
                else:
                    next
        except:
            pass

    data_time = datetime.today()
    _id = data_time.strftime("%Y") + data_time.strftime("%m") + \
        data_time.strftime("%d")+data_time.strftime("%H") + \
        data_time.strftime("%M")
    Prelist_Mongo_insert(lista, constant_band, market_cap, _id)
    print('---Pre_List process Done---')
    #return [_id, lista]


def hierarchy(lista, cash, _id, id_process):
    print('\x1b[6;30;46m' + '*********** Start Hierarchy *******************' + '\x1b[0m')
    # -------------------------------------------------------
    # Verify that the list has a good spread to take into account in this process
    str_list = ''
    spread_variable = 0.02
    for x in range(0, len(lista)-1):
        str_list = lista[x]+', '+str_list
    str_list += lista[-1]
    cycle_book_data=True
    while cycle_book_data:
        try:
            book_data_result = book_data(str_list)
            cycle_book_data=False
        except:
            time.sleep(10)
    cash = 25000
    result = {}
    lista_result = []
    for data in book_data_result['data'][0]['content']:
        bids = data['2']
        asks = data['3']
        symbol = data['key']
        total = cash
        for ask in asks:
            total = total - (float(ask['0'])*float(ask['1']))
            if total < 0:
                value = (ask['0']-bids[0]['0'])/ask['0']
                if value < spread_variable:
                    result[symbol] = value
                    lista_result.append(symbol)
                    break
    # -------------------------------------------------------

    final_data = {}
    json_book_data = {}
    today = (dt.datetime.today()+dt.timedelta(1)).strftime('%Y-%m-%d')
    hist = (dt.datetime.today()-dt.timedelta(7)).strftime('%Y-%m-%d')
    r = {'ADX': [], 'TENDENCY': [], 'CDL3INSIDE': [], 'CDLENGULFING': [], 'CDLGAPSIDESIDEWHITE': [], 'CDLHAMMER': [], 'CDLSHORTLINE': [], 'CDLUNIQUE3RIVER': [],
         'VOLUME': [], 'MARKET_VALUE': [], 'ATR': []}
    data = pd.DataFrame(data=r)

    r = {'symbol': [], 'result': [], 'ATR': [], 'close': [], 'qty': []}
    result = pd.DataFrame(data=r)

    r = {'ATR': []}
    ATR = pd.DataFrame(data=r)

    r = {'close': []}
    close = pd.DataFrame(data=r)

    for symbol in lista_result:
        cycle = True
        while cycle:
            try:
                df = yf.download(symbol, interval='90m',
                                 start=hist, end=today, threads=False, progress=False)
                df = df.rename(columns={"Open": "open", "High": "high",
                                        "Low": "low", "Close": "close", "Volume": "volume"})
                cycle = False
            except:
                time.sleep(5)
                
                continue

        ADX = talib.ADX(
            df['high'], df['low'], df['close'], timeperiod=7)
        data.loc[symbol, 'ADX'] = ADX[-1]
        data.loc[symbol, 'TENDENCY'] = (
            df['close'][-1]-df['close'][0])/(df['close'][0])
        CDL3INSIDE = talib.CDL3INSIDE(
            df['open'][-5:], df['high'][-5:], df['low'][-5:], df['close'][-5:])
        data.loc[symbol, 'CDL3INSIDE'] = CDL3INSIDE.sum()

        CDLENGULFING = talib.CDLENGULFING(
            df['open'][-5:], df['high'][-5:], df['low'][-5:], df['close'][-5:])
        data.loc[symbol, 'CDLENGULFING'] = CDLENGULFING.sum()

        CDLGAPSIDESIDEWHITE = talib.CDLGAPSIDESIDEWHITE(
            df['open'][-5:], df['high'][-5:], df['low'][-5:], df['close'][-5:])
        data.loc[symbol, 'CDLGAPSIDESIDEWHITE'] = CDLGAPSIDESIDEWHITE.sum()

        CDLHAMMER = talib.CDLHAMMER(
            df['open'][-5:], df['high'][-5:], df['low'][-5:], df['close'][-5:])
        data.loc[symbol, 'CDLHAMMER'] = CDLHAMMER.sum()

        CDLSHORTLINE = talib.CDLSHORTLINE(
            df['open'][-5:], df['high'][-5:], df['low'][-5:], df['close'][-5:])
        data.loc[symbol, 'CDLSHORTLINE'] = CDLSHORTLINE.sum()

        CDLUNIQUE3RIVER = talib.CDLUNIQUE3RIVER(
            df['open'][-5:], df['high'][-5:], df['low'][-5:], df['close'][-5:])
        data.loc[symbol, 'CDLUNIQUE3RIVER'] = CDLUNIQUE3RIVER.sum()

        data.loc[symbol, 'ATR'] = talib.ATR(
            df['high'], df['low'], df['close'], timeperiod=14)[-5:].mean()/df['close'][-5:].mean()
        ATR.loc[symbol, 'ATR'] = data.loc[symbol, 'ATR']
        data.loc[symbol, 'VOLUME'] = df['volume'].mean()
        data.loc[symbol, 'MARKET_VALUE'] = df['volume'].mean() * \
            df['close'].mean()
        close.loc[symbol, 'close'] = df['close'][0]
        r = data.to_json(orient='split')
        parsed = json.loads(r)
        final_data[symbol] = parsed
    #vector = [1/11]*11
    # ADX, TENDENCY, CDL3INSIDE, CDLENGULFING, CDGAPSIDESIDEWHITE, CDLHAMMER, CDLSHORTLINE, CDLUNIQUE3RIVER, VOLUME, MARKET_VALUE, ATR
    vector=[0.05,0.20,0.07,0.05,0.09,0.09,0.09,0.09,0.09,0.09,0.09]
    #print(data)
    for i in data.columns:
        if data[i].sum() != 0:
            data[i] = data[i]/data[i].sum()

    for j, i in enumerate(data.index):
        # here I included a paterns filter. I have to check if this works.
        if paterns(i, condition_reversal_patterns=True,condition_pattern_down=True,condition_pattern_up=False) > 0:
            result.loc[j, 'symbol'] = i
            result.loc[j, 'ATR'] = ATR.loc[i, 'ATR']
            result.loc[j, 'result'] = sum(data.loc[i]*vector)
            result.loc[j, 'close'] = close.loc[i, 'close']
    list_sort = result.sort_values(
        'result', ascending=False).reset_index(drop=True)

    for i in range(0, len(list_sort['symbol'])):
        list_sort.loc[i, 'qty'] = int(cash/list_sort.loc[i, 'close'])-1

    Hierarchy_Mongo_insert(
        list(list_sort['symbol']), _id, id_process, final_data, json_book_data)
    print('---Ready Hierarchy---')
    return list_sort.reset_index(drop=True)


def select(symbols, cash, _id, id_process):
    print('\x1b[6;30;46m' + '*********** Start Select *******************'+ '\x1b[0m')
    review = []
    r = {'upperband': [], 'middleband': [], 'lowerband': [],
         'macd': [], 'macdsignal': [], 'macdhist': [], 'rsi': [], 'sma10': [], 'sma40': [], 'stock': [], 'close': []}
    resultado = pd.DataFrame(data=r)
    today = (dt.datetime.today()+dt.timedelta(1)).strftime('%Y-%m-%d')
    hist = (dt.datetime.today()-dt.timedelta(20)).strftime('%Y-%m-%d')
    final_data = {}
    for symbol in symbols:
        try:
            # ------------------
            # GET DATA
            df = yf.download(symbol, interval='90m',
                             start=hist, end=today, threads=False, progress=False)
            df = df.rename(columns={"Open": "open", "High": "high",
                                    "Low": "low", "Close": "close", "Volume": "volume"})
            # ------------------
            # df = pd.read_csv('ivan2.csv')
            df['upperband'], df['middleband'], df['lowerband'] = talib.BBANDS(df['close'],
                                                                              timeperiod=20, nbdevup=2,
                                                                              nbdevdn=2, matype=0)

            # df = df.set_index('Date', drop=True)
            # print(df)
            data = df.iloc[[-1], :]
            if (data['close'].values > data['lowerband'].values and data['open'].values < data['lowerband'].values) or (data['close'].values < data['lowerband'].values and data['open'].values > data['lowerband'].values):
                review.append(symbol)
            else:
                data = df.iloc[[-2], :]
                if (data['close'].values > data['lowerband'].values and data['open'].values < data['lowerband'].values) or (data['close'].values < data['lowerband'].values and data['open'].values > data['lowerband'].values):
                    review.append(symbol)
                else:
                    if df.iloc[[-2], 3].values > df.iloc[[-2], 0].values:
                        for i in range(3, 5):
                            data = df.iloc[[-i], :]
                            if (data['close'].values > data['lowerband'].values and data['open'].values < data['lowerband'].values) or (data['close'].values < data['lowerband'].values and data['open'].values > data['lowerband'].values):
                                if df.iloc[[-2], 3].values > data['close'].values and df.iloc[[-2], 3].values > data['open'].values:
                                    df['macd'], df['macdsignal'], df['macdhist'] = talib.MACD(df['close'],
                                                                                              fastperiod=12, slowperiod=26, signalperiod=9)
                                    df['rsi'] = talib.RSI(
                                        df['close'], timeperiod=14)
                                    df['sma10'] = talib.SMA(
                                        df['close'], timeperiod=10)
                                    df['sma40'] = talib.SMA(
                                        df['close'], timeperiod=40)
                                    r = df.to_json(orient='split')
                                    parsed = json.loads(r)
                                    final_data[symbol] = parsed
                                    data = df.iloc[[-1], :]
                                    data = data.assign(stock=symbol)
                                    # print(data.index[0])
                                    # data['stock'] = [symbol]
                                    resultado = resultado.append(data)
                    else:
                        pass
        except Exception as e:
            print(e)
            print('Error')
            time.sleep(2)
            continue

    # Filter because the patter

    # Filter because the patter
    if resultado.empty:
        r = {'symbol': [], 'result': [], 'ATR': [],
             'close': [], 'qty': []}
        hierarchy_result = pd.DataFrame(data=r)
        rr = []
        Select_Mongo_insert(rr, _id, id_process, final_data)
        print('---Ready Select but we do not have select Data---')
    else:
        r = resultado['stock'].values
        Select_Mongo_insert(list(r), _id, id_process, final_data)
        print('---Ready Select---')
        hierarchy_result = hierarchy(resultado['stock'], cash, _id, id_process)
    return hierarchy_result
