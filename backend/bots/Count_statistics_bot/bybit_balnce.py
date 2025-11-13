import sqlite3
from datetime import datetime
from pybit.unified_trading import HTTP
import schedule
import time

# Название базы данных
db_name = 'balance.db'

# Функция для вставки данных в БД
def insert_balance(balance: float, timestamp: int):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS balance (id INTEGER PRIMARY KEY AUTOINCREMENT, balance REAL, timestamp INTEGER)")
    cursor.execute("INSERT INTO balance (balance, timestamp) VALUES (?, ?)", (balance, timestamp))
    conn.commit()
    conn.close()

# Функция для получения баланса с Bybit
def bybit_balance():
    api_key = 'rixIdgl13et1dCa8pX'  # Укажите ваш API-ключ
    api_secret = 'Dvy76elR0ZAFjklSUhPfqpnjzAFlxPSRCLTR'  # Укажите ваш секретный ключ

    session = HTTP(
        testnet=False,  # Установите в True, если используете тестовую сеть
        api_key=api_key,
        api_secret=api_secret,
    )

    try:
        response = session.get_wallet_balance(accountType='UNIFIED')
        balance = float(response['result']['list'][0]['totalWalletBalance'])
        timestamp = response['time']
        insert_balance(balance, timestamp)
        print(f"Баланс успешно сохранён: {balance}, Время: {timestamp}")
    except Exception as e:
        print(f"Ошибка при получении баланса: {e}")

# bybit_balance()

# # Запланировать выполнение функции в 10:00 утра каждый день
schedule.every().day.at("21:00").do(bybit_balance)

if __name__ == "__main__":
    print("Balance Bybit")
    while True:
        schedule.run_pending()
        time.sleep(10)  # Проверяем задачи каждую минуту
