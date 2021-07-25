from Alpaca import *
from Components import *
import time
from datetime import datetime
import csv
from Mongo import *
import threading





def watch(percent=0.2):
    print('\x1b[6;30;43m' + '*********** Start Watch *******************' + '\x1b[0m')

    cycle = True
    if percent > 0.1:
        percent=0.1
    while cycle:
        buy_data = Buy_Mongo_last_data()
        id_process = buy_data['id_process']
        id_prelist = buy_data['id_prelist']
        qty = buy_data['qty']
        try:
            if float(buy_data['qty_remnant']) != 0:
                sell_order = watch_sell(id_process, percent)
                try:
                    Sell_Mongo_insert(
                        sell_order.client_order_id, sell_order.qty, sell_order.__dict__['_raw'],  id_prelist, id_process)
                except:
                    Sell_Mongo_insert('Stop Lost', qty,
                                      'Stop Lost',  id_prelist, id_process)
            else:
                print('--- All Stocks are already sold ---')
            cycle = False
        except:
            pass
    print('watch')
# -----------------------------------------------------------------------------------------------
def buy(symbol, qty, _id, id_process, percent=0.5):
    print('\x1b[6;30;43m' + '*********** Start Buy *******************' + '\x1b[0m')

    print(symbol)
    print(qty)
    print(percent)
    print(datetime.today())
    if percent > 0.1:
        percent=0.1
    try:
        cycle=False
        cycle_paterns=True
        while cycle_paterns:
            if paterns(symbol, condition_reversal_patterns=False,condition_pattern_down=False,condition_pattern_up=True) > 400:
                cycle_paterns=False
                buy_order = order_buy(symbol=symbol, qty=qty)
                cycle = True
                while cycle:
                    try:
                        stop_lost_order = order_stop_lost(
                            symbol=symbol, qty=qty, percent=percent)
                        cycle = False
                    except:
                        #print('Error Stop Lost Order')
                        time.sleep(3)
                        pass
                delete_list.append(symbol)
                try:
                    Buy_Mongo_insert(stop_lost_order.client_order_id, buy_order.client_order_id,
                                    buy_order.qty,  buy_order.__dict__['_raw'], stop_lost_order.__dict__['_raw'], _id, id_process)
                except:
                    pass
                watch(percent=0.2)
            else:
                time.sleep(10)
    except Exception as err:
        print(err)
        pass
    
    
    
    
def watch_and_buy(symbol, qty, _id, id_process, percent=0.5):
    print('\x1b[6;30;43m' + '*********** Start Watch and Buy *******************' + '\x1b[0m')


def funtion_pre_select():
    x = datetime.today()
    y = x.replace(day=x.day, hour=16, minute=30)
    y = y.strftime("%m/%d/%Y, %H:%M")
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M")
    while date_time < y:
        pre_select() 
        now = datetime.now()
        date_time = now.strftime("%m/%d/%Y, %H:%M")
# Dwn here you can find all the general process

if __name__ == '__main__':
    thread = threading.Thread(target=funtion_pre_select)
    thread.start()
    percent=0.3
    delete_list=[]
    x = datetime.today()
    y = x.replace(day=x.day, hour=16, minute=30)
    y = y.strftime("%m/%d/%Y, %H:%M")
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M")
    empty = 0
    time_data = (datetime(now.year, now.month,
                        now.day, 9, 30, 0) - now)
    sleep_time = time_data.seconds
    days = time_data.days
    if days >= 0:
        if sleep_time > 0:
            print(f'Mosel wait { sleep_time } seconds')
            time.sleep(sleep_time)
    count = 0
    
    while date_time < y:
    #while date_time != y:
        _id = Prelist_Mongo_last_data()['_id'] 
        account, posittion = get_info()
        if not posittion:
            list_check = True
            while list_check:
                lista = Prelist_Mongo_last_data()['list']
                _id = Prelist_Mongo_last_data()['_id'] 
                if lista:
                    print('---Pre_List is Ready---')
                    list_check = False
                else:
                    print('---Pre_List is not Ready yet---')
                    time.sleep(10)
            for dele_symbol in delete_list:
                if dele_symbol in lista:
                    lista.remove(dele_symbol)
        #print('delete ')
        #print(delte_list)
        count += 1
        id_process = _id + '_' + str(count)
        account, posittion = get_info()
        if not posittion:
            hierarchy_result = select(
                lista, float(account.cash), _id, id_process)
            #print(hierarchy_result)
            if hierarchy_result.empty:
                time.sleep(100)
            else:
                empty = 0
                # print(hierarchy_result)
                qty = hierarchy_result.loc[0, 'qty']
                # qty = 100
                percent = hierarchy_result.loc[0, 'ATR']*100
                percent = percent/2
                if percent < 0.1:
                    percent = 0.1
                if posittion:
                    watch_and_buy(
                        hierarchy_result.loc[0, 'symbol'], qty, _id, id_process, percent)
                else:
                    buy(hierarchy_result.loc[0, 'symbol'],
                        qty, _id, id_process, percent)
            del hierarchy_result
        else:
            watch(percent)
            time.sleep(10)
            print('.... Fin')
        now = datetime.now()
        date_time = now.strftime("%m/%d/%Y, %H:%M")