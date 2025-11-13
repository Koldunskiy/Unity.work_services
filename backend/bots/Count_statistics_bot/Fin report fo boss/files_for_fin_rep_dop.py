GVIDO_1 = 4_000
GVIDO_2 = 4_200

ANREY = 100_000
NITSAN = 103_000
# Гвидо 1, Гвидо 2
from dop_file import get_binance_balance

import time
import requests
import hmac
import hashlib
import urllib.parse
import datetime

broker_name_dict = {
    'Гвидо 1': {
        "API Key": "njG4q2UEA2L8cA2cF6TR4VS3c5KX0MfYk3mi6Pcw4MRTmvVOffyBj7y0Xb6PcWFz", 
        "Secret Key": "L2Cfv3wh5syrvPUlihCmFq6KY4hF7gT4dITkmsg88Rrr5EhQODQS1HNUIYCIFWya"
    },
    'Гвидо 2': {
        "API Key": "C6fhlaRyXJFjC3vH1o2VwlsGmwHz8TE3u2RIpXqFLh3AHg9DBlIBR8jV9rABbVUT", 
        "Secret Key": "UoX0F5lm7oWfHUmoQHqr6RtLFEuRmB9LG81ckFT9MRJChzKz5MexgmxDn6hh2AWt"
    },
    'Петр': {
        "API Key": "ZaEc9cnlQsevjPpOUEnsCEHMKYB5SLPck5Jjj2o0Yhow6SILDWwwOgLvoZRfaswx", 
        "Secret Key": "RyviXIMVdxmc8RYWMQaC0zUTUFGwBTW21mxFWA9jENHbWBOqZ1ij2yNFVbvAGC4B"
    }
}

def get_account_snapshot(api_key, secret_key, snapshot_type='SPOT', start_time=None, end_time=None, limit=30):
    """
    Получает снимки аккаунта с Binance.
    
    :param api_key: Ваш API ключ.
    :param secret_key: Ваш секретный ключ.
    :param snapshot_type: Тип аккаунта ('SPOT', 'MARGIN', 'FUTURES'). Здесь используется 'SPOT'.
    :param start_time: Начальное время в миллисекундах (опционально).
    :param end_time: Конечное время в миллисекундах (опционально).
    :param limit: Количество записей (максимум 30).
    :return: JSON-ответ от Binance.
    """
    base_url = "https://api.binance.com"
    endpoint = "/sapi/v1/accountSnapshot"
    timestamp = int(time.time() * 1000)

    params = {
        "type": snapshot_type,
        "timestamp": timestamp,
        "limit": limit
    }
    if start_time is not None:
        params["startTime"] = start_time
    if end_time is not None:
        params["endTime"] = end_time

    query_string = urllib.parse.urlencode(params)
    signature = hmac.new(secret_key.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    query_string += "&signature=" + signature

    url = base_url + endpoint + "?" + query_string
    headers = {
        "X-MBX-APIKEY": api_key
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    return data

def parse_snapshot_data(snapshot_data):
    """
    Извлекает даты и баланс (totalAssetOfBtc) из полученных данных.
    
    :param snapshot_data: JSON-ответ от Binance.
    :return: Два списка – даты (datetime) и балансы (float).
    """
    snapshots = snapshot_data.get("snapshotVos", [])
    dates = []
    balances = []
    
    for snap in snapshots:
        update_time = snap.get("updateTime")
        dt = datetime.datetime.fromtimestamp(update_time / 1000.0)
        dates.append(dt)
        # Для спотового счёта в data содержится поле totalAssetOfBtc
        total_asset = float(snap.get("data", {}).get("assets", 0)[0]['walletBalance'])
        balances.append(total_asset)
    return dates, balances



def get_binance_balance(day : int, snapshot_type: str, broker_name: str) -> str:
    """
    Получаем динамику баланса по счету Бинанса
    :param day: временной интервал, на сколько дней смотреим назад
    :snapshot_type: Тип кошелька, который будем смотреть. 'SPOT', 'MARGIN', 'FUTURES' 
    :broker_name:  Имя Трейдера """ 
    # Замените на ваши API-ключ и секретный ключ
    api_key = broker_name_dict[broker_name]["API Key"]
    secret_key = broker_name_dict[broker_name]["Secret Key"]

    

    # Задаём временной интервал: последние 30 дней
    now = int(time.time() * 1000)
    thirty_days_ago = now - day * 24 * 60 * 60 * 1000

    # Получаем снимки аккаунта
    snapshot_data = get_account_snapshot(api_key, secret_key, snapshot_type=snapshot_type, 
                                         start_time=thirty_days_ago, end_time=now, limit=30)
    
    # Если произошла ошибка, можно вывести сообщение
    if snapshot_data.get("code") != 200 :
        raise Exception  ("Ошибка при получении данных:", snapshot_data)
    elif len(snapshot_data.get("snapshotVos", 0)) == 0:
        raise Exception ('На данном кошельке данных пока нет.')
    else:
        # Обрабатываем данные и строим график
        dates, balances = parse_snapshot_data(snapshot_data)
        return (dates, balances)
    

def count_profit(dates: list[str], balance: list[float], CONST):
    '''date - дата 
    ration_local - отношение д-1 / д-2
    ration_global - д-1 / сonst
    '''
    
    date = dates[1].strftime("%d.%m.%Y")
    ration_local = f'{((balance[1] / balance[0]) - 1) * 100:.2f} %'
    ration_global = f'{((balance[1] / CONST) - 1) * 100:.2f} %'
    
    return (date, ration_local, ration_global) 
# gvido_1 = count_profit(*get_binance_balance(2, 'FUTURES', 'Гвидо 1'), CONST=GVIDO_1)
# gvido_2 = count_profit(*get_binance_balance(2, 'FUTURES', 'Гвидо 2'), CONST=GVIDO_2)

# get_binance_balance(2, 'FUTURES', 'Гвидо 1')
# Андрей
import sqlite3
from pybit.unified_trading import HTTP
import numpy as np

def get_dynamic_balance_bybit():
    conn = sqlite3.connect("balance.db")
    cursor = conn.cursor()
    cursor.execute("SELECT balance, timestamp FROM balance WHERE ID > (SELECT MAX(ID) - 2 FROM balance);")
    result  = cursor.fetchall()
    conn.close()
    result = np.array(result)
    balance = result[ :, 0]
    timestamps = [datetime.datetime.fromtimestamp(timestamp / 1000) for timestamp in result[ :, 1]]
    return  timestamps, balance
# Andery = count_profit(*get_dynamic_balance_bybit(), CONST=ANREY)
# Andery

# Антон
def Unity_hist_balanc(accaunt: int, headers: dict):
    'Функция, которая считает баланс аккаунтов за вчера и позавчера'
    data_finish = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    data_start = (datetime.datetime.now() - datetime.timedelta(days=2)).strftime("%Y-%m-%d")
    
    url = f'https://rest.unity.finance/api/v1/balanceHistory?accountId={accaunt}&assetId=1&from={data_start}&to={data_finish}'
    answer = requests.get(url, headers=headers)
    return answer.json()


def count_balance_Unity(accaunts: list, token: str, count_sum: bool = False):
    'Функция считате абсолютные и процентные изменения аккаунтов Ю за вчера и позовчера'
    headers = {'accept': 'application/json', 'auth-token': token}
    massiv = []

    for accaunt in accaunts:
        massiv.extend(Unity_hist_balanc(accaunt, headers))

    sum_two_days_ago = sum([i['balance'] for i in  massiv[::2]])  # 2025-04-08
    sum_one_days_ago = sum([i['balance'] for i in  massiv[1::2]]) # 2025-04-09

    if count_sum:
        return sum_one_days_ago

    absolut_znach = sum_one_days_ago - sum_two_days_ago
    try:
        prozent_znach = f'{((sum_one_days_ago / sum_two_days_ago) - 1) * 100:.2f} %'
    except:
        prozent_znach = '0 %'

    return absolut_znach, prozent_znach
Neo_MU_Key = '8c75f6a6-d3e6-4257-b6e5-4513f36975b9'
Neo_KZ_Key = '08d238f9-2af9-4cd7-8d95-e0bcb2f050a8'
ARK_Capital_Key = '41da8163-8e10-4b8d-be5e-9b01f3a7304d'

Neo_MU_accaunts = [1889, 2296, 2522, 2760, 3175, 5220, 5264, 5662]  # по идее основной
Neo_KZ_accaunts = [3314, 3315, 3316, 4769]
ARK_Capital_accaunts = [4976]

Unity_Server_percev_accaunts = [5242, 5243]

headers = {'accept': 'application/json', 'auth-token': Neo_MU_Key}
# Neo_MU_absolut, Neo_MU_prozent = count_balance_Unity(Neo_MU_accaunts, Neo_MU_Key)
# Neo_KZ_absolut, Neo_KZ_prozent = count_balance_Unity(Neo_KZ_accaunts, Neo_KZ_Key)
# ARK_Capital_absolut, ARK_Capital_prozent = count_balance_Unity(ARK_Capital_accaunts, ARK_Capital_Key)

# res_summ_Anton = sum(count_balance_Unity(accs, key, True)
#                for accs, key in ((Neo_MU_accaunts, Neo_MU_Key),
#                                  (Neo_KZ_accaunts, Neo_KZ_Key),
#                                  (ARK_Capital_accaunts, ARK_Capital_Key)))
# Nitsan
import mysql.connector

# Конфигурация подключения
CONFIG_1 = {
    'user': 'neo_reports',
    'password': 'gh2uyti56hgk2h',
    'host': '92.38.186.22',
    'port': '3306',
    'database': 'mt5r1',  # не забудь указать имя БД!
    'raise_on_warnings': True
}

# SQL-запросы
profit_yesterday = '''
SELECT SUM(Profit) AS profit_yesterday
FROM mt5_deals
WHERE login = 902148 AND DATE(Time) = CURDATE() - INTERVAL 1 DAY;
'''

profit_day_before_yesterday = '''
SELECT SUM(Profit) AS profit_day_before_yesterday
FROM mt5_deals
WHERE login = 902148 AND DATE(Time) = CURDATE() - INTERVAL 2 DAY;
'''

total_profit = '''
SELECT SUM(Profit) AS total_profit
FROM mt5_deals
WHERE login = 902148;
'''

# Функция получения значений
def get_Nitsan_profits():
    connection = mysql.connector.connect(**CONFIG_1)
    cursor = connection.cursor()

    cursor.execute(profit_yesterday)
    py = cursor.fetchone()[0] or 0  # если None, вернёт 0

    cursor.execute(profit_day_before_yesterday)
    pdy = cursor.fetchone()[0] or 0

    cursor.execute(total_profit)
    tp = cursor.fetchone()[0] or 0

    cursor.close()
    connection.close()

    ration_day = ((py / pdy) - 1) * 100 if pdy != 0 else 0
    reatio_global = ((tp / NITSAN) - 1) * 100

    return ration_day, reatio_global

# Пример вызова
# Nitsan_dayly, Nitsan_global = get_Nitsan_profits()

