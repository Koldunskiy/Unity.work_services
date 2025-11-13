
# headers = {'accept': 'application/json', 'auth-token': '8c75f6a6-d3e6-4257-b6e5-4513f36975b9'}

# 2024-10-16 time example
import requests
import json
import numpy as np
from typing import List, Tuple
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Используем бэкенд для рендеринга графиков без GUI


def account_balance_for_account(headers: dict, accaunt_id: int) -> dict:
    link = f'https://rest.unity.finance/api/v1/accountBalance?accountId={accaunt_id}'
    answer = requests.get(link, headers=headers)
    return answer.json()

def balance_history_for_time_interval(headers: dict, accaunt_id: int, time_start: str, end_time: str) -> dict:
    link = f'https://rest.unity.finance/api/v1/balanceHistory?accountId={accaunt_id}&assetId=1&from={time_start}&to={end_time}'
    answer = requests.get(link, headers=headers)
    return answer.json()


def count_all_accaunts(headers: dict, accaunts: List) -> Tuple[float]:
    '''Считаем totalAssets и prevTotalAssets'''
    totalAssets = []
    prevTotalAssets = []
    for accaunt in accaunts:
        d = account_balance_for_account(headers, accaunt)
        totalAssets.append(d['totalAssets'])
        prevTotalAssets.append(d['prevTotalAssets'])
    totalAssets = np.array(totalAssets)
    prevTotalAssets = np.array(prevTotalAssets)
    return round(totalAssets.mean(),2),  round(prevTotalAssets.mean(),2)

def count_all_history_accaunts(headers: dict, accaunts: List, time_start: str, end_time: str) -> pd.Series:
    result = []
    for accaunt in accaunts:
        data = balance_history_for_time_interval(headers, accaunt, time_start, end_time)
        balances = [item['balance'] for item in data]
        result.append(balances)
    time_series = [item['date'] for item in data]
    try:
        df = pd.DataFrame(result, columns=time_series)
        return df.mean(axis=0)
    except Exception as e:
        raise ValueError(f"Не могу получить данные. Вероятно не закрыты дни в диапазоне {time_start} - {end_time}.")
    

# Функция для создания и сохранения графика
def build_graphs(data: pd.Series, filename="graph.png"):
    plt.figure(figsize=(10, 7))
    plt.plot(data.keys().tolist(), data.tolist(), marker='o')
    plt.grid(True)
    plt.legend(['PNL'])
    plt.ylabel('USD')
    plt.xlabel('Date')
    date_start, date_finish = data.keys().tolist()[0], data.keys().tolist()[-1]
    plt.title(f'Total Balance (Assets)\n{date_start} - {date_finish}')
    plt.xticks(rotation=90)

    # Сохраняем график в файл
    plt.savefig(filename)
    plt.close()  # Закрываем график для освобождения памяти


import re

def validate_date_string(date_string):
    # Шаблон регулярного выражения для формата 'yyyy-mm-dd, yyyy-mm-dd'
    pattern = r'^\d{2}-\d{2}-\d{4},\s*\d{2}-\d{2}-\d{4}$'
    date_string = date_string.strip()
    # Проверяем, соответствует ли строка шаблону
    if re.match(pattern, date_string):
        return True
    else:
        return False
    
def Total_Open_Positions(headers: dict, accaunts: List) -> int:
    res = []
    for accaunt in accaunts:
        link = f'https://rest.unity.finance/api/v1/listActiveOrders?accountId={accaunt}'
        answer = requests.get(link, headers=headers)
        answer = answer.json()['items']
        if answer != []:
            df = pd.DataFrame(answer)
            res.append(df['amount'].sum())


    return sum(res)


def unrelizPNL(headers: dict, accaunts: list) -> int:
    unPNL = 0
    for accaunt in accaunts:
        link = f'https://rest.unity.finance/api/v1/accountPositions?accountId={accaunt}&currency=1'
        answer = requests.get(link, headers=headers).json()['positions']
        if answer != []:
            unPNL += answer[0]['unrealizedConvertedPnL']
    return unPNL



def count_dayly_PNL_and_make_graphs(headers, accaunts: List, time_start: str, end_time: str) -> float:
    balance = count_all_history_accaunts(headers, accaunts, time_start, end_time)
    daily_profit  = balance - balance.shift(1)
    colors = ['green' if profit > 0 else 'red' for profit in daily_profit]

    # Построение графика
    plt.figure(figsize=(10, 7))
    plt.bar(daily_profit.index, daily_profit, color=colors)
    plt.title('Ежедневная прибыль')
    plt.xlabel('Дата')
    plt.ylabel('Прибыль')
    plt.xticks(rotation=90)
    plt.grid(True)
    plt.tight_layout()

    # Сохраняем график в файл
    plt.savefig('graph2.png')
    plt.close()  # Закрываем график для освобождения памяти
    return daily_profit.sum()

import datetime
import calendar

# Функция для получения начала и конца текущей недели
def get_current_week(smechenie_dny3=0):
    today = datetime.date.today()
    start_of_week = today - datetime.timedelta(days=today.weekday() + smechenie_dny3)  # Понедельник текущей недели
    end_of_week = start_of_week + datetime.timedelta(days=6)  # Воскресенье текущей недели
    return start_of_week.strftime('%Y-%m-%d'), end_of_week.strftime('%Y-%m-%d')

# Функция для получения начала и конца прошлой недели
def get_last_week(smechenie_dny3=0, smechenie_dny1=0):
    today = datetime.date.today()
    start_of_last_week = today - datetime.timedelta(days=today.weekday() + 7 + smechenie_dny3)  # Понедельник прошлой недели
    end_of_last_week = start_of_last_week + datetime.timedelta(days=6 + smechenie_dny1)  # Воскресенье прошлой недели
    return start_of_last_week.strftime('%Y-%m-%d'), end_of_last_week.strftime('%Y-%m-%d')

# Функция для получения начала и конца текущего месяца
def get_current_month():
    today = datetime.date.today()
    start_of_month = today.replace(day=1)  # Первый день текущего месяца
    last_day = calendar.monthrange(today.year, today.month)[1]  # Последний день текущего месяца
    end_of_month = today.replace(day=last_day)  # Последний день текущего месяца
    return start_of_month.strftime('%Y-%m-%d'), end_of_month.strftime('%Y-%m-%d')

# Функция для получения начала и конца прошлого месяца
def get_last_month():
    today = datetime.date.today()
    first_day_of_current_month = today.replace(day=1)
    last_day_of_last_month = first_day_of_current_month - datetime.timedelta(days=1)  # Последний день прошлого месяца
    start_of_last_month = last_day_of_last_month.replace(day=1)  # Первый день прошлого месяца
    return start_of_last_month.strftime('%Y-%m-%d'), last_day_of_last_month.strftime('%Y-%m-%d')

# ============================================================================

import time
import requests
import hmac
import hashlib
import urllib.parse
import datetime
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

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


import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plot_balance_history(dates, balances, snapshot_type):
    """
    Строит детализированный график динамики баланса в высоком разрешении (4K).
    
    :param dates: Список дат.
    :param balances: Список значений баланса.
    :param snapshot_type: Может быть 'SPOT', 'MARGIN', 'FUTURES'.
    """
    plt.figure(figsize=(20, 10), dpi=300)  # 4K-разрешение

    # Основная линия баланса
    plt.plot(dates, balances, marker='o', linestyle='-', color='blue', linewidth=2, markersize=8, label="Баланс (USDT)")

    # Добавление значений баланса на график
    for i in range(len(dates)):
        plt.text(dates[i], balances[i], f"{balances[i]:,.2f}", fontsize=12, verticalalignment='bottom', horizontalalignment='left', rotation=45)

    # Настройка осей
    plt.xlabel("Дата", fontsize=16, fontweight="bold")
    plt.ylabel("Баланс (USDT)", fontsize=16, fontweight="bold")
    plt.title(f"Динамика баланса {snapshot_type} на Binance", fontsize=18, fontweight="bold")

    # Форматирование оси X
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.xticks(rotation=45, fontsize=14)
    plt.yticks(fontsize=14)
    
    # Сетка
    plt.grid(True, linestyle="--", alpha=0.7)

    # Легенда
    plt.legend(fontsize=14)

    # Отступы для красивого отображения
    plt.tight_layout()

    # Сохраняем график в файл с высоким качеством
    plt.savefig('Binance_walet.png', dpi=300, bbox_inches='tight')
    
    # Закрываем график для освобождения памяти
    plt.close()

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


def calculate_balance_changes(dates, balances):
    # Получаем текущую дату и текущий баланс
    current_balance = balances[-1]
    current_date = dates[-1]

    # Функция для расчета процента изменения
    def calculate_percentage_change(start_balance, end_balance):
        return (end_balance - start_balance) / start_balance * 100

    # Разница за сегодня
    today_balance = balances[-1]
    today_date = current_date.date()
    previous_day_balance = None
    
    # Ищем баланс за предыдущий день
    for i in range(len(dates) - 1, -1, -1):
        if dates[i].date() != today_date:
            previous_day_balance = balances[i]
            break
            
    if previous_day_balance is not None:
        change_today = calculate_percentage_change(previous_day_balance, today_balance)
    else:
        change_today = 0  # если нет данных за предыдущий день

    # Разница за текущую неделю
    # Вычисляем начало текущей недели (с понедельника)
    start_of_week = current_date - datetime.timedelta(days=current_date.weekday())  # Понедельник текущей недели
    week_start_balance = None
    
    # Ищем баланс за начало недели
    for i in range(len(dates) - 1, -1, -1):
        if dates[i] < start_of_week:  # Если дата меньше начала недели
            week_start_balance = balances[i]
            break
            
    if week_start_balance is not None:
        change_week = calculate_percentage_change(week_start_balance, today_balance)
    else:
        change_week = 0  # если нет данных за неделю

    # Разница за текущий месяц
    # Ищем индекс начала месяца, то есть первое число месяца
    month_start_balance = None
    for i in range(len(dates) - 1, -1, -1):
        if dates[i].month != current_date.month:
            # Когда месяц меняется, значит предыдущая дата - это первое число текущего месяца
            month_start_balance = balances[i + 1]
            break
    
    if month_start_balance is not None:
        change_month = calculate_percentage_change(month_start_balance, today_balance)
    else:
        change_month = 0  # если нет данных за месяц

 
    change_30_days = calculate_percentage_change(balances[0], today_balance)
   

    # Формируем ответ
    answer = f''' 
Изменение баланса:
Баланс: {today_balance:,.2f} USD
1) за сегодня: {change_today:.1f}%
2) за текущую неделю: {change_week:.1f}%
3) за текущий месяц: {change_month:.1f}%
4) за последние 30 дней: {change_30_days:.1f}%
'''.replace(",", ' ')
    return answer



def get_binance_balance(day : int, snapshot_type: str, broker_name: str) -> str:
    """
    Получаем динамику баланса по счету Бинанса
    :param day: временной интервал, на сколько дней смотреим назад
    :snapshot_type: Тип кошелька, который будем смотреть. 'SPOT', 'MARGIN', 'FUTURES' 
    :broker_name:  Имя Трейдера """ 
    # Замените на ваши API-ключ и секретный ключ
    api_key = broker_name_dict[broker_name]["API Key"]
    secret_key = broker_name_dict[broker_name]["Secret Key"]

    if snapshot_type == 'MARGIN':
        return margin_wallet(api_key, secret_key)

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
        plot_balance_history(dates, balances, snapshot_type)
        return calculate_balance_changes(dates, balances)
    
#==================================================
# ByBit
import sqlite3
from pybit.unified_trading import HTTP

def bybit_balance():
    api_key = 'rixIdgl13et1dCa8pX'  # Укажите ваш API-ключ
    api_secret = 'Dvy76elR0ZAFjklSUhPfqpnjzAFlxPSRCLTR'  # Укажите ваш секретный ключ

    session = HTTP(
        testnet=False,  # Установите в True, если используете тестовую сеть
        api_key=api_key,
        api_secret=api_secret,
    )

    response = session.get_wallet_balance(accountType='UNIFIED')
    balance = round(float(response['result']['list'][0]['totalWalletBalance']), 2)
    timestamp = response['time']
    dt_object = datetime.datetime.fromtimestamp(timestamp / 1000)
    formatted_date = dt_object.strftime("%d-%m-%Y")  # Формат: день-месяц-год
    # Форматируем баланс с разделением тысяч пробелами и округлением до 2 знаков
    formatted_balance = f"{balance:,.2f}".replace(",", " ")
    # Формируем строку
    string = f"На {formatted_date} баланс составляет: {formatted_balance} USD"
    return string

import numpy as np

def get_dynamic_balance_bybit():
    conn = sqlite3.connect("balance.db")
    cursor = conn.cursor()
    cursor.execute("SELECT balance, timestamp FROM balance ")
    result  = cursor.fetchall()
    conn.close()
    result = np.array(result)
    balance = result[ :, 0]
    timestamps = [datetime.datetime.fromtimestamp(timestamp / 1000) for timestamp in result[ :, 1]]
    plot_balance_history(timestamps, balance, '')
    calculate_balance = calculate_balance_changes(timestamps, balance)
    return calculate_balance



#Binance, Margin счет. Автоматически подставляються ключи Петра
import requests
import time
import hmac
import hashlib
from urllib.parse import urlencode

BASE_URL = 'https://api.binance.com'

def sign_request(params, api_secret):
    query_string = urlencode(params)
    signature = hmac.new(api_secret.encode('utf-8'),
                         query_string.encode('utf-8'),
                         hashlib.sha256).hexdigest()
    params['signature'] = signature
    return params

def get_cross_margin_balance_requests(api_key, api_secret):
    endpoint = '/sapi/v1/margin/account'
    url = BASE_URL + endpoint
    params = {'timestamp': int(time.time() * 1000)}
    params = sign_request(params, api_secret)
    headers = {'X-MBX-APIKEY': api_key}
    response = requests.get(url, params=params, headers=headers)
    result = "Кросс-маржинальные балансы:\n"
    if response.status_code == 200:
        data = response.json()
        for asset in data.get('userAssets', []):
            if float(asset['netAsset']) != 0:
                result += (f"{asset['asset']}: свободно: {asset['free']}, "
                           f"заем: {asset['borrowed']}, чистый баланс: {asset['netAsset']}\n")
        if result.strip() == "Кросс-маржинальные балансы:":
            result += "Нет активов с ненулевым балансом."
    else:
        result = f"Ошибка получения кросс-маржинального баланса: {response.text}"
    return result

def get_isolated_margin_balance_requests(api_key, api_secret):
    endpoint = '/sapi/v1/margin/isolated/account'
    url = BASE_URL + endpoint
    params = {'timestamp': int(time.time() * 1000)}
    params = sign_request(params, api_secret)
    headers = {'X-MBX-APIKEY': api_key}
    response = requests.get(url, params=params, headers=headers)
    result = "Изолированные маржинальные балансы:\n"
    if response.status_code == 200:
        data = response.json()
        for pair in data.get('assets', []):
            result += f"Пара {pair['symbol']}:\n"
            result += (f"  Базовый актив - свободно: {pair['baseAsset']['free']}, "
                       f"заем: {pair['baseAsset']['borrowed']}\n")
            result += (f"  Котируемый актив - свободно: {pair['quoteAsset']['free']}, "
                       f"заем: {pair['quoteAsset']['borrowed']}\n")
    else:
        result = f"Ошибка получения изолированного маржинального баланса: {response.text}"
    return result

def margin_wallet(api_key='ZaEc9cnlQsevjPpOUEnsCEHMKYB5SLPck5Jjj2o0Yhow6SILDWwwOgLvoZRfaswx', api_secret='RyviXIMVdxmc8RYWMQaC0zUTUFGwBTW21mxFWA9jENHbWBOqZ1ij2yNFVbvAGC4B'):
    cross_margin_str = get_cross_margin_balance_requests(api_key, api_secret)
    isolated_margin_str = get_isolated_margin_balance_requests(api_key, api_secret)
    combined_result = cross_margin_str + "\n-----------------\n" + isolated_margin_str
    return combined_result
