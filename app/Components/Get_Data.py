from Alpaca.Alpaca_API import *
import talib
import yfinance as yf
import time
import pandas as pd


symbols = get_list()
review = []
r = {'open': [], 'high': [], 'low': [], 'close': [],  'Adj Close': [], 'volume': [], 'upperband': [], 'middleband': [], 'lowerband': [],
     'macd': [], 'macdsignal': [], 'macdhist': [], 'rsi': [], 'sma10': [], 'sma40': [], 'profitability': [], 'time_profitability': [], 'lost': [], 'time_lost': [], 'stock': []}
resultado = pd.DataFrame(data=r)
#symbols = ['ASAXU']
for symbol in symbols:
    print(symbol)
    try:
        # ------------------
        # GET DATA
        """df = get_bar(symbol, start='1/1/2021',
                    end='2021-03-05', time='15Min', limit=1000)
        df = df[symbol]
        """
        df = yf.download(symbol, start='2020-1-1',
                         end='2021-3-5', interval='1h')
        # df = yf.download(symbol, interval='1D')
        df = df.rename(columns={"Open": "open", "High": "high",
                                "Low": "low", "Close": "close", "Volume": "volume"})
        # ------------------
        a = df['volume']*df['close']
        if a.mean() < 2000000:
            next
        df['upperband'], df['middleband'], df['lowerband'] = talib.BBANDS(df['close'],
                                                                          timeperiod=20, nbdevup=2,
                                                                          nbdevdn=2, matype=0)
        df['macd'], df['macdsignal'], df['macdhist'] = talib.MACD(df['close'],
                                                                  fastperiod=12, slowperiod=26, signalperiod=9)
        df['rsi'] = talib.RSI(df['close'], timeperiod=14)
        df['sma10'] = talib.SMA(df['close'], timeperiod=10)
        df['sma40'] = talib.SMA(df['close'], timeperiod=40)
        df.to_csv('df.csv')

    except:
        pass

    incluir = False
    incluir2 = False
    for i in range(4, len(df)-40):
        data = df.iloc[[-i], :]
        if (data['close'].values > data['lowerband'].values and data['open'].values < data['lowerband'].values) or (data['close'].values < data['lowerband'].values and data['open'].values > data['lowerband'].values):
            incluir = True
            for j in range(1, 4):
                data2 = df.iloc[[-i+j], :]
                if (data2['close'].values > data2['lowerband'].values and data2['open'].values < data2['lowerband'].values) or (data2['close'].values < data2['lowerband'].values and data2['open'].values > data2['lowerband'].values):
                    incluir = False

            if incluir is True:
                incluir2 = False
                sign = 0
                for j in range(1, 4):
                    data2 = df.iloc[[-i+j], :]
                    if data2['close'].values > data2['open'].values:
                        if data2['close'].values > data['close'].values and data2['close'].values > data['open'].values:
                            sign = j
                            incluir2 = True
                            break
                if incluir2 is True:
                    cycle = True
                    buy = df.iloc[[-i+sign+1], 0].values
                    # print(df.iloc[[-i+sign+1]])
                    close = buy
                    sell_lost = close
                    high = close
                    time = 0
                    sell = 0
                    maximum = 0
                    time_lost = 0
                    if time + i == 0:
                        cycle = False
                    while cycle is True:
                        minimum = high*0.98
                        time += 1
                        if time - i + sign == -1:
                            cycle = False
                        close = df.iloc[[-i+sign+time], 3].values
                        high = df.iloc[[-i+sign+time], 1].values
                        if close <= minimum:
                            # print(df.iloc[[-i+sign+1], 0])
                            # print(df.iloc[[-i+sign+time], 3])
                            cycle = False
                            sell_lost = close
                            time_lost = time
                        if close >= maximum:
                            maximum = close
                            time_profitability = time

                    data.loc[data.index[0], 'lost'] = (sell_lost-buy)/buy
                    data.loc[data.index[0], 'time_lost'] = time_lost
                    data.loc[data.index[0], 'profitability'] = (
                        maximum-buy)/buy
                    data.loc[data.index[0],
                             'time_profitability'] = time_profitability
                    data.loc[data.index[0], 'stock'] = symbol
                    resultado = resultado.append(data)

    """print('ivan')
    print(resultado)
    print(resultado['profitability'].sum())
    print(resultado['lost'].sum())"""
resultado.to_csv('resultado.csv')
