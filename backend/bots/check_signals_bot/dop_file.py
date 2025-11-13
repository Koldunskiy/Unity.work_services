import sqlite3
import pandas as pd
import numpy as np
from binance.client import Client
from datetime import datetime, timedelta


def get_hist_data(symbol: str, start_time: str) -> pd.DataFrame:
    """Загружает исторические свечи с Binance.

    Использует 5-минутный интервал. Возвращает DataFrame с OHLC.

    Args:
        symbol (str): Торговый символ (например, 'BTCUSDT').
        start_time (str): Время начала в формате ISO (например, '2024-01-01 00:00:00').

    Returns:
        pd.DataFrame: DataFrame с колонками ['Open time', 'Open', 'High', 'Low', 'Close'].
    """
    api_key = 'd1bc948a8af0c74cc5c746f68e5b63bf21ab8789533b637eb6f80d754508b66a'
    api_secret = '81929ddcab087592ac2ce85d1a6933b9379f2fcf458077b85fb7d0666ab23b13'
    client = Client(api_key, api_secret)

    interval = Client.KLINE_INTERVAL_5MINUTE
    end_time = None

    candles = client.get_historical_klines(symbol, interval, start_time, end_time)

    df = pd.DataFrame(
        candles,
        columns=[
            'Open time', 'Open', 'High', 'Low', 'Close', 'Volume',
            'Close Time', 'Quote Asset Volume', 'Number of Trades',
            'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume', 'Ignore'
        ]
    )

    df['Open time'] = pd.to_datetime(df['Open time'], unit='ms')
    df.drop([
        'Volume', 'Close Time', 'Quote Asset Volume', 'Number of Trades',
        'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume', 'Ignore'
    ], axis=1, inplace=True)

    df[['Open', 'High', 'Low', 'Close']] = df[['Open', 'High', 'Low', 'Close']].apply(
        pd.to_numeric, errors='coerce'
    )

    return df


def Strategy_Tester_v3(
    start_time: pd.Timestamp,
    df: pd.DataFrame,
    side: str,
    price: float,
    stop_loss: float,
    take_profit1: float,
    take_profit2: float = None,
    open_order_type: str = 'Limit'
) -> tuple:
    """Тестирует торговую стратегию с двумя тейк-профитами.

    Проверяет вход, SL, TP1, TP2. Ограничивает проверку 24 часами.
    Возвращает результат и временные метки.

    Args:
        start_time (pd.Timestamp): Время создания сигнала.
        df (pd.DataFrame): Исторические данные.
        side (str): 'Buy' или 'Sell'.
        price (float): Цена входа.
        stop_loss (float): Уровень стоп-лосса.
        take_profit1 (float): Первый тейк-профит.
        take_profit2 (float, optional): Второй тейк-профит. Defaults to None.
        open_order_type (str): Тип ордера (не используется в логике). Defaults to 'Limit'.

    Returns:
        tuple: Результат теста:
            - Для TP/SL/EXP: (status, time_enter, time_close, duration, price_close)
            - Для NOT_ENTER: ['NOT_ENTER']
    """
    df = df[df['Open time'] >= start_time].reset_index(drop=True)

    side = side.capitalize()
    is_buy = side == 'Buy'

    PRICE_INDICATOR = False
    STOP_LOSS_INDICATOR = False
    TAKE_PROFIT1_INDICATOR = False
    TAKE_PROFIT2_INDICATOR = False

    approximate_time_enter = None
    approximate_time_TP1 = None
    approximate_time_TP2 = None
    approximate_time_SL = None

    for _, row in df.iterrows():
        # Ограничение по времени — 24 часа
        if row['Open time'] >= start_time + pd.Timedelta(hours=24):
            return ["NOT_ENTER"]

        # === Проверка входа ===
        if not PRICE_INDICATOR:
            if (is_buy and row['Low'] <= price) or (not is_buy and row['High'] >= price):
                PRICE_INDICATOR = True
                approximate_time_enter = row['Open time']
            else:
                continue  # Пропускаем, пока не вошли

        # === Проверка Stop Loss ===
        if (is_buy and row['Low'] <= stop_loss) or (not is_buy and row['High'] >= stop_loss):
            STOP_LOSS_INDICATOR = True
            approximate_time_SL = row['Open time']

            if TAKE_PROFIT1_INDICATOR:
                return (
                    "TP1",
                    approximate_time_enter,
                    approximate_time_TP1,
                    (approximate_time_TP1 - approximate_time_enter),
                    take_profit1
                )
            return (
                "SL",
                approximate_time_enter,
                approximate_time_SL,
                (approximate_time_SL - approximate_time_enter),
                stop_loss
            )

        # === Проверка TP1 ===
        if not TAKE_PROFIT1_INDICATOR:
            if (is_buy and row['High'] >= take_profit1) or (not is_buy and row['Low'] <= take_profit1):
                TAKE_PROFIT1_INDICATOR = True
                approximate_time_TP1 = row['Open time']

        # === Проверка TP2 ===
        if take_profit2 and not TAKE_PROFIT2_INDICATOR:
            if (is_buy and row['High'] >= take_profit2) or (not is_buy and row['Low'] <= take_profit2):
                TAKE_PROFIT2_INDICATOR = True
                approximate_time_TP2 = row['Open time']
                return (
                    "TP2",
                    approximate_time_enter,
                    approximate_time_TP2,
                    (approximate_time_TP2 - approximate_time_enter),
                    take_profit2
                )

        # === Если сработал только TP1 ===
        if TAKE_PROFIT1_INDICATOR and not TAKE_PROFIT2_INDICATOR:
            return (
                "TP1",
                approximate_time_enter,
                approximate_time_TP1,
                (approximate_time_TP1 - approximate_time_enter),
                take_profit1
            )

    # === Если позиция осталась открытой до конца данных ===
    if PRICE_INDICATOR:
        last_price = row['Close']
        approximate_time_EXP = row['Open time']
        return (
            "EXP",
            approximate_time_enter,
            approximate_time_EXP,
            (approximate_time_EXP - approximate_time_enter),
            last_price
        )

    return ["NOT_ENTER"]


def main_fun() -> None:
    """Основная функция: читает сигналы из БД, тестирует их и обновляет статус."""
    conn = sqlite3.connect('trading_analysis.db')
    df = pd.read_sql(
        'SELECT * FROM Trade_Signals WHERE is_check = 0 OR is_check = 3',
        con=conn
    )
    df.drop(['analyseType', 'header', 'body'], axis=1, inplace=True)

    # Округляем время до ближайших 5 минут
    df['createTime'] = pd.to_datetime(df['createTime'])
    df['createTime'] = df['createTime'].dt.floor('T') - pd.to_timedelta(
        df['createTime'].dt.minute % 5, unit='m'
    )
    df['foreCast'] = df['foreCast'].replace({'Up': 'Buy', 'Down': 'Sell'})

    results = []

    for symbol in df['instrumentId'].unique():
        min_time = df[df['instrumentId'] == symbol]['createTime'].min()
        hist_data = get_hist_data(symbol=symbol, start_time=str(min_time))

        for _, row in df[df['instrumentId'] == symbol].iterrows():
            enter_price = row['entry']
            tp1 = row['tp1']
            tp2 = row['tp2']
            sl = row['sl']

            if pd.notna(enter_price) and pd.notna(tp1) and pd.notna(sl):
                tp2_val = tp2 if pd.notna(tp2) else None
                result = list(Strategy_Tester_v3(
                    start_time=row['createTime'],
                    df=hist_data,
                    side=row['foreCast'],
                    price=enter_price,
                    stop_loss=sl,
                    take_profit1=tp1,
                    take_profit2=tp2_val
                ))
                result.insert(0, row['id'])  # Добавляем ID
                results.append(result)
            else:
                results.append([row['id'], 'incorrect data'])

    # === Обновление БД ===
    conn = sqlite3.connect('trading_analysis.db')
    cursor = conn.cursor()

    for values in results:
        if len(values) == 6:  # Полный результат
            status = values[1]
            is_check = 3 if status == 'EXP' else 1
            sql = '''
                UPDATE Trade_Signals 
                SET status = ?, time_enter = ?, time_close = ?, duration = ?, price_close = ?, is_check = ?
                WHERE id = ?
            '''
            cursor.execute(sql, (
                status,
                str(values[2]),
                str(values[3]),
                str(values[4]),
                values[5],
                is_check,
                values[0]
            ))
        else:  # Ошибка или NOT_ENTER
            sql = 'UPDATE Trade_Signals SET status = ?, is_check = 1 WHERE id = ?'
            cursor.execute(sql, (values[1], values[0]))

    conn.commit()
    conn.close()