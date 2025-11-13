import requests
import pandas as pd
from datetime import datetime, timedelta
import mysql.connector
import numpy as np
import logging
from process_data import send_message

# Конфигурирование логгера
logging.basicConfig(
    filename='Unity_bot_ideas.log',
    level=logging.WARNING,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

CONFIG = {
    'user': 'tester',
    'password': 'Fx123456#',
    'host': '192.168.1.6',
    'port': '3306',
    'raise_on_warnings': True
}
UNITY_KEY = 'c3f28d5b-9694-4307-b30f-6f800ee13506'

from process_data import load_data
import time
import json

with open('right_instumets.json', 'r', encoding='utf-8') as f:
    RIGHT_INSTRUMENTS = json.load(f)


def Strategy_Tester(
        data: list,
        side: str,
        open_order_type: str,
        stop_loss: float,
        price: float,
        take_profit: float
) -> tuple:
    """Тестирует стратегию на исторических данных.

    Проверяет условия входа, стоп-лосса и тейк-профита.
    Возвращает результат (TP, SL, EXP или NOT_ENTER) с деталями.

    Args:
        data (list): Список исторических данных (OHLC).
        side (str): Направление сделки ('Buy' или 'Sell').
        open_order_type (str): Тип ордера ('Limit' или 'Stop').
        stop_loss (float): Уровень стоп-лосса.
        price (float): Цена входа.
        take_profit (float): Уровень тейк-профита.

    Returns:
        tuple: Результат теста (статус, цена закрытия, P/L, времена и т.д.).
    """
    side, open_order_type = side.capitalize(), open_order_type.capitalize()
    df = pd.DataFrame(data)
    # Преобразование timestamp в формат datetime с учетом часового пояса UTC
    df['timestamp2'] = pd.to_datetime(df['timestamp'], unit='ms').dt.tz_localize('UTC')
    # Преобразуем дату в формат "d-m-Y H:M:S" и создадим новый столбец 'formatted_date'
    df['formatted_date'] = df['timestamp2'].dt.strftime('%Y-%m-%d %H:%M:%S')
    df = df.drop(columns=["timestamp2"])
    df[["close", "high", "low", "open"]] = df[["close", "high", "low", "open"]].apply(pd.to_numeric, errors='coerce')
    df = df[::-1]
    df = df.reset_index(drop=True)
    '''Алгоритм проверки'''
    new_df = df.copy()
    PRICE_INDICATOR = False
    STOP_LOSS_INDICATOR = False
    TAKE_PROFIT_INDICATOR = False
    # 1. Проверяем вход по цене
    if side == 'Buy':
        Flag = True
        if open_order_type == 'Limit':
            price_open = new_df[new_df['low'] <= price]
        else:
            price_open = new_df[new_df['high'] >= price]
    else:
        Flag = False
        if open_order_type == 'Limit':
            price_open = new_df[new_df['high'] >= price]
        else:
            price_open = new_df[new_df['low'] <= price]

    if not price_open.empty:
        index_price = price_open.index[0]
        new_df = new_df.iloc[index_price:].reset_index(drop=True)
        PRICE_INDICATOR = True
        approximate_time_enter, accurate_time_enter = price_open['formatted_date'].iloc[0], \
        price_open['timestamp'].iloc[0]
    # 2. Проверяем стоп-лосс
    if Flag:
        stop_loss_res = new_df[new_df['low'] <= stop_loss]
    else:
        stop_loss_res = new_df[new_df['high'] >= stop_loss]

    if not stop_loss_res.empty:
        index_stop_loss = stop_loss_res.index[0]
        new_df = new_df.iloc[:index_stop_loss + 1].reset_index(drop=True)
        STOP_LOSS_INDICATOR = True
        approximate_time_ST, accurate_time_ST = stop_loss_res['formatted_date'].iloc[0], \
        stop_loss_res['timestamp'].iloc[0]

    # 3. Проверяем на take profit
    if Flag:
        take_profit_res = new_df[new_df['high'] >= take_profit]
    else:
        take_profit_res = new_df[new_df['low'] <= take_profit]

    if not take_profit_res.empty:
        take_profit_index = take_profit_res.index[0]
        TAKE_PROFIT_INDICATOR = True
        approximate_time_TP, accurate_time_TP = take_profit_res['formatted_date'].iloc[0], \
        take_profit_res['timestamp'].iloc[0]

    def timedelta(str1: str, str2: str) -> str:
        """Вычисляет разницу между двумя датами в формате HH:MM:SS.

        Args:
            str1 (str): Начальная дата.
            str2 (str): Конечная дата.

        Returns:
            str: Разница в формате HH:MM:SS.
        """
        date_format = '%Y-%m-%d %H:%M:%S'
        date1 = datetime.strptime(str1, date_format)
        date2 = datetime.strptime(str2, date_format)
        # Вычисление разницы между датами
        time_difference = date2 - date1
        # Извлечение часов, минут и секунд из разницы
        hours, remainder = divmod(time_difference.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        # Форматирование результатов
        result_string = '{:02}:{:02}:{:02}'.format(hours, minutes, seconds)
        return result_string

    # 4. Вывод
    if PRICE_INDICATOR:
        if TAKE_PROFIT_INDICATOR:
            return ("TP", take_profit, abs(take_profit - price), approximate_time_enter, approximate_time_TP,
                    timedelta(approximate_time_enter, approximate_time_TP))
        elif STOP_LOSS_INDICATOR and not TAKE_PROFIT_INDICATOR:
            return ("SL", stop_loss, -1 * abs(stop_loss - price), approximate_time_enter, approximate_time_ST,
                    timedelta(approximate_time_enter, approximate_time_ST))
        else:
            last_price = new_df['close'].iloc[-1]
            approximate_time_EXP = new_df['formatted_date'].iloc[-1]
            return ("EXP",
                    last_price,
                    last_price - price if side == 'Buy' else price - last_price,
                    approximate_time_enter,
                    approximate_time_EXP,
                    timedelta(approximate_time_enter, approximate_time_EXP))
    else:
        return ('NOT_ENTER',)


class Tester_Bot:
    def __init__(self) -> None:
        """Инициализирует Tester_Bot с настройками для API и базы данных."""
        self.link_UNITY_select_all_active_ideas = 'https://rest.unity.finance/api/v1/tradeIdeas?limit=1000&statuses=ACTIVE'
        self.table_name = 'tradeideas.unity_data'

    @staticmethod
    def Unity_api(link: str) -> list:
        """Делает запрос к Unity API.

        Args:
            link (str): URL для запроса.

        Returns:
            list: JSON-ответ от API.
        """
        headers = {'auth-token': UNITY_KEY}
        response = requests.get(link, headers=headers)
        return response.json()

    def main_process_data(self) -> pd.DataFrame:
        """Обрабатывает данные из Unity API и вставляет их в БД.

        Проверяет на дубликаты и вставляет только новые записи.

        Returns:
            pd.DataFrame: Обработанный DataFrame (для отладки).
        """
        try:
            'Данный метод комплексно обрабатывает данные. Потом данные вставляються в БД, предварительно проверяться на наличе уже сделанной записи.'
            d = Tester_Bot.Unity_api(self.link_UNITY_select_all_active_ideas)
            df = pd.DataFrame(d['items'])

            df['expirationTime'] = pd.to_datetime(df['expirationTime'], format='mixed')
            df['expirationTime'] = df['expirationTime'].dt.strftime("%Y-%m-%d %H:%M:%S")
            df['createTime'] = pd.to_datetime(df['createTime'], format='mixed')
            df['createTime'] = df['createTime'].dt.strftime("%Y-%m-%d %H:%M:%S")

            df['instrumentIds'] = df['instrumentIds'].apply(lambda x: x[0])
            # ===================================
            instrumentIds = df['instrumentIds'].tolist()
            instrumentIds = ",".join(map(str, instrumentIds))

            link = f'https://rest.unity.finance/api/v1/instrumentDetails?instrumentId={instrumentIds}'
            data = Tester_Bot.Unity_api(link)
            df_instruments = pd.DataFrame(data['items'])
            df = pd.merge(df, df_instruments, left_on='instrumentIds', right_on='id', how='left')
            df["instrumentIds"] = df['code']
            # ============================

            df = df.drop(['brokerId', 'status', 'publishTime', 'updateTime', 'id_y', 'code'], axis=1)
            df.columns = ['unity_id', 'instrument', 'open_order_type', 'side', 'open_order_price', 'stop_loss',
                          'take_profit', 'confidence', 'expiration_time', 'description_text', 'create_time', "source",
                          "provider", "state", "subscribers", "priority", "rate"]
            # ============================
            table_name = 'tradeideas.unity_data'
            connection = mysql.connector.connect(**CONFIG)
            cursor = connection.cursor()

            cursor.execute('SELECT unity_id FROM tradeideas.unity_data')
            id_unity_spisok = np.array(cursor.fetchall()).flatten()

            columns_name = list(map(lambda x: x[0], df.columns.tolist()))
            for index, row in df.iterrows():
                unity_id = row['unity_id']
                if len(((df['instrument'].iloc[index]).tolist())[0]) <= 35:
                    if unity_id not in id_unity_spisok:
                        values = [str(value) for value in row.tolist()]

                        sql_query = f"INSERT INTO {table_name} ({', '.join(columns_name)}) VALUES ({', '.join(['%s'] * len(columns_name))})"

                        # Исполнение SQL-запроса
                        cursor.execute(sql_query, tuple(values))
            connection.commit()
            cursor.close()
            connection.close()
        except Exception as e:
            logging.warning(f'В 1 блоке - обработке данных по API Unity ошибка - {e}')

    def take_necessary_data(self) -> list:
        """Забирает данные из БД для тестирования стратегий.

        Тестирует каждую запись и возвращает результаты.

        Returns:
            list: Список результатов тестов стратегий.
        """
        'Шаг 2. Забираем нужные нам данные из БД и провекряем их'
        connection = mysql.connector.connect(**CONFIG)
        sql_query = '''
                    SELECT id, \
                           instrument, \
                           side, \
                           open_order_type, \
                           open_order_price, \
                           stop_loss, \
                           take_profit, \
                           create_time, \
                           expiration_time
                    FROM tradeideas.unity_data
                    WHERE expiration_time <= NOW() \
                      and report is NULL;'''
        check_df = pd.read_sql(sql_query, connection)
        connection.close()
        # ИЗМЕНЯЕМ ВРЕМЯ НА НОРМАЛЬНОЕ
        check_df['expiration_time'] = (
            pd.to_datetime(check_df['expiration_time'], format="%Y-%m-%d %H:%M:%S")).dt.strftime("%d.%m.%Y %H:%M:%S")
        check_df['create_time'] = (pd.to_datetime(check_df['create_time'], format="%Y-%m-%d %H:%M:%S")).dt.strftime(
            "%d.%m.%Y %H:%M:%S")
        check_df.set_index('id', inplace=True)
        # Проверка данных
        strategy_result = []
        for idx, row in check_df.iterrows():
            instrument, side, open_order_type, open_order_price, stop_loss, take_profit, create_time, expiration_time = row
            if instrument in RIGHT_INSTRUMENTS:
                instrument = RIGHT_INSTRUMENTS[instrument]
            try:
                data = load_data(instrument, create_time, expiration_time)
                result = Strategy_Tester(data, side, open_order_type, stop_loss, open_order_price, take_profit)
                strategy_result.append((idx, result, 'OK'))
                time.sleep(60)
            except Exception as e:
                time.sleep(60)
                strategy_result.append((idx, 'Неизвестный запрос для Exante API'))
                logging.warning(f'В 2 блоке - проверке данных ошибка - {e}')
        return strategy_result

    def update_tabel(self, strategy_result: list) -> None:
        """Обновляет таблицу в БД результатами тестов.

        Args:
            strategy_result (list): Список результатов для обновления.
        """
        'Шаг 3. Запись в БД'
        try:
            connection = mysql.connector.connect(**CONFIG)
            cursor = connection.cursor()
            sql_2 = '''UPDATE tradeideas.unity_data \
                       SET current_state = %s, \
                           current_price = %s, \
                           pl            = %s, \
                           open_time     = %s, \
                           close_time    = %s, \
                           DURATION      = %s, \
                           report        = %s
                       WHERE id = %s \
                    '''

            for row in strategy_result:
                if len(row) == 3:
                    idx, value, report = row
                    if isinstance(value, tuple):
                        value = list(value)
                        value.extend([report, idx])
                        cursor.execute(sql_2, tuple(value))

                    else:
                        request = 'UPDATE tradeideas.unity_data SET current_state = %s, report = %s where id = %s'
                        cursor.execute(request, (value, report, idx))

                else:
                    idx, report = row
                    request = 'UPDATE tradeideas.unity_data SET report = %s where id = %s'
                    cursor.execute(request, (report, idx))
        except Exception as e:
            logging.warning(f'В 3 блоке - запись данных в БД ошибка - {e}')

        # Подтвердите изменения
        connection.commit()

        # Закройте курсор и соединение
        cursor.close()
        connection.close()


def report_every_day() -> None:
    """Генерирует и отправляет ежедневный отчет по данным из БД."""
    connection = mysql.connector.connect(**CONFIG)
    sql = '''
          SELECT expiration_time, current_state, report, pl
          FROM tradeideas.unity_data
          WHERE expiration_time BETWEEN DATE_SUB(CURDATE(), INTERVAL 1 DAY) AND CURDATE();'''
    df = pd.read_sql(sql, connection)
    connection.close()
    if not df.empty:
        # ==================
        total_records = len(df)
        dct = df['current_state'].value_counts().to_dict()
        unknow_methods = df['report'].value_counts().get('Неизвестный запрос для Exante API', 0)
        EXP_positiv = len(df[(df['current_state'] == 'EXP') & (df['pl'] > 0)])
        date = str(df['expiration_time'].iloc[0])[:10]
        # ==================
        s = f'''Всего получено сигналов: {total_records} за {date}
Из них:
- Успешно прошли проверку: {total_records - unknow_methods}
- Нет инструмента на Exante: {unknow_methods}

По итогу проверки из {total_records - unknow_methods} прошедших проверку:
- Take profit = {dct.get('TP', 0)}
- Stop Loss = {dct.get('SL', 0)}
- Не сработали вовсе = {dct.get('NOT_ENTER', 0)}
- На момент экспирации была открытая позиция = {dct.get('EXP', 0)}
- Из них {EXP_positiv} закрыты в Profit и {dct.get('EXP', 0) - EXP_positiv} в Loss'''
        send_message(s)