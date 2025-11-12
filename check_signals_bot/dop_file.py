import sqlite3
import pandas as pd
from binance.client import Client
from datetime import datetime
import numpy as np
# Подключение к базе данных
def get_hist_data(symbol: str, start_time: str) -> pd.DataFrame:
    api_key = 'd1bc948a8af0c74cc5c746f68e5b63bf21ab8789533b637eb6f80d754508b66a'
    api_secret = '81929ddcab087592ac2ce85d1a6933b9379f2fcf458077b85fb7d0666ab23b13'
    client = Client(api_key, api_secret)
    interval = Client.KLINE_INTERVAL_5MINUTE 
    end_time = None
    candles = client.get_historical_klines(symbol, interval, start_time, end_time)
    df = pd.DataFrame(candles, columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume',
                                        'Close Time', 'Quote Asset Volume', 'Number of Trades',
                                        'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume', 'Ignore'])
    df['Open time'] = pd.to_datetime(df['Open time'], unit='ms')
    df.drop(['Volume', 'Close Time', 'Quote Asset Volume', 'Number of Trades', 'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume', 'Ignore'], axis=1, inplace=True)
    df[['Open', 'High', "Low", 'Close']] = df[['Open', 'High', "Low", 'Close']].apply(pd.to_numeric, errors='coerce')
    return df



def Strategy_Tester_v3(start_time: pd.Timestamp, df: pd.DataFrame, side: str, price: float, stop_loss: float, take_profit1: float, take_profit2: float = None, open_order_type: str = 'Limit') -> tuple:
    df = df[df['Open time'] >= start_time].reset_index(drop=True)
    
    side, open_order_type = side.capitalize(), open_order_type.capitalize()
    PRICE_INDICATOR = False
    STOP_LOSS_INDICATOR = False
    TAKE_PROFIT1_INDICATOR = False
    TAKE_PROFIT2_INDICATOR = False
    approximate_time_TP1, approximate_time_TP2, approximate_time_SL = None, None, None


    # Флаг направления сделки
    flag_buy = side == 'Buy'

    approximate_time_enter = None

    for i, row in df.iterrows():

        if row['Open time'] >= start_time + pd.Timedelta(hours=24):
            return ["NOT_ENTER"] 

        # Проверяем вход по цене
        if not PRICE_INDICATOR:
            if (flag_buy and row['Low'] <= price) or (not flag_buy and row['High'] >= price):
                PRICE_INDICATOR = True
                approximate_time_enter = row['Open time']
            else:
                continue  # Пока не вошли в позицию, пропускаем строку

        # Проверяем SL, TP1, TP2
        if PRICE_INDICATOR:
            # Проверка Stop Loss
            if (flag_buy and row['Low'] <= stop_loss) or (not flag_buy and row['High'] >= stop_loss):
                STOP_LOSS_INDICATOR = True
                approximate_time_SL = row['Open time']

                if TAKE_PROFIT1_INDICATOR: # если вдруг TP1 отработал, а потом сработал стоп лосс
                    return ("TP1", approximate_time_enter, approximate_time_TP1, (approximate_time_TP1 - approximate_time_TP1), take_profit1)

                return ("SL", approximate_time_enter, approximate_time_SL, (approximate_time_SL - approximate_time_enter), stop_loss)

            # Проверка Take Profit 1
            if not TAKE_PROFIT1_INDICATOR:
                if (flag_buy and row['High'] >= take_profit1) or (not flag_buy and row['Low'] <= take_profit1):
                    TAKE_PROFIT1_INDICATOR = True
                    approximate_time_TP1 = row['Open time']

            if take_profit2:
            # Проверка Take Profit 2
                if not TAKE_PROFIT2_INDICATOR:
                    if (flag_buy and row['High'] >= take_profit2) or (not flag_buy and row['Low'] <= take_profit2):
                        TAKE_PROFIT2_INDICATOR = True
                        approximate_time_TP2 = row['Open time']
                        return ("TP2", approximate_time_enter, approximate_time_TP2, (approximate_time_TP2 - approximate_time_enter), take_profit2)

            # Если достигнут только TP1
            if TAKE_PROFIT1_INDICATOR and not TAKE_PROFIT2_INDICATOR:
                return ("TP1",  approximate_time_enter, approximate_time_TP1, (approximate_time_TP1 - approximate_time_enter), take_profit1)

    # Если не было выполнено ни одно из условий (SL, TP1, TP2), возвращаем EXP
    if PRICE_INDICATOR:
        last_price = row['Close']
        approximate_time_EXP = row['Open time']
        return ("EXP", approximate_time_enter, approximate_time_EXP, (approximate_time_EXP - approximate_time_enter), last_price)

    return ["NOT_ENTER"] 



def main_fun():
    conn = sqlite3.connect('trading_analysis.db')
    df = pd.read_sql('select * from Trade_Signals where is_check = 0 or is_check = 3', con=conn)
    df.drop(['analyseType', 'header', 'body'], axis=1, inplace=True)
    df['createTime'] = pd.to_datetime(df['createTime'])
    df['createTime'] = df['createTime'].dt.floor('T') - pd.to_timedelta(df['createTime'].dt.minute % 5, unit='m')
    df['foreCast'] = df['foreCast'].replace({'Up' : 'Buy', 'Down': 'Sell'})
# =======================================
    
    res = []
    for symbol in df['instrumentId'].unique():
        min_time = df[df['instrumentId'] == symbol]['createTime'].min()
        data = get_hist_data(symbol=symbol, start_time=str(min_time))

        for index, row in df[df['instrumentId'] == symbol].iterrows():
            enter_price = row['entry']
            tp1 = row['tp1']
            tp2 = row['tp2']
            sl = row['sl']
            if not np.isnan(enter_price) and not np.isnan(tp1) and not np.isnan(sl):
                if np.isnan(tp2):
                    tp2 = None
                result = list(Strategy_Tester_v3(
                    start_time=row['createTime'],
                    df=data,
                    side=row['foreCast'],
                    price=enter_price,
                    stop_loss=sl,
                    take_profit1=tp1,
                    take_profit2=tp2
                ))
                # Добавляем `id` к результату
                result.insert(0, row['id'])
                res.append(result)
            else:
                res.append([row['id'], 'incorrect data'])

    # Подключаемся к базе данных
    conn = sqlite3.connect('trading_analysis.db')
    cursor = conn.cursor()
    
    sql2 = 'UPDATE Trade_Signals SET status = ?, is_check = 1  WHERE id = ?'
    for values in res:
        if len(values) == 6:
            is_check = 3 if values[1] == 'EXP' else 1
            sql1 = f'UPDATE Trade_Signals SET status = ?, time_enter = ?, time_close = ?, duration = ?, price_close = ?, is_check = {is_check} WHERE id = ?'
            cursor.execute(sql1, (values[1], str(values[2]), str(values[3]), str(values[4]), values[5], values[0]))
        else:
            cursor.execute(sql2, (values[1],  values[0]))

    # Сохранение изменений и закрытие соединения
    conn.commit()
    conn.close()

