import pandas as pd
import yfinance as yf
import datetime as dt

df = pd.read_csv('./Data/Active_Stocks.csv')
today = (dt.datetime.today()+dt.timedelta(1)).strftime('%Y-%m-%d')
hist = (dt.datetime.today()-dt.timedelta(20)).strftime('%Y-%m-%d')
good_list = []
for symbol in df['symbol']:
    df = yf.download(symbol, interval='1h', start=hist,
                     end=today, threads=False)
    if list(df.index):
        good_list.append(symbol)

good_list = pd.DataFrame(good_list, columns=['symbol'])
good_list.to_csv('./Data/Good_List.csv')
