from pybit.unified_trading import HTTP
import pandas as pd
import requests
import os
import datetime
import logging
import time

import requests

def send_telegram_message(message: str):
    bot_token = "7699618218:AAHEjT-wxs1aV8beVLDKiiOWq1--ZMEXqNM"
    chat_id = -4752383371
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    }

    response = requests.post(url, json=payload)

# --- Настройка логирования ---
LOG_FILE = "app.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

# --- Глобальные переменные ---
TOKEN = 'f20a0f07-2680-43b1-af6e-c0ff9a770418'
SYMBOLS_FILE = "U_SYMBOLS_ID.csv"
accaunts = [2447, 2448, 2449]
# API ByBit
api_key="rixIdgl13et1dCa8pX"
api_secret="Dvy76elR0ZAFjklSUhPfqpnjzAFlxPSRCLTR"


def load_symbols_id():
    """Загружает symbols_id из CSV-файла и возвращает словарь."""
    if not os.path.exists(SYMBOLS_FILE):
        # Если файла нет, создаем пустой DataFrame и сохраняем его
        pd.DataFrame(columns=['symbol', 'u_id']).to_csv(SYMBOLS_FILE, index=False)
        logging.warning(f"Файл {SYMBOLS_FILE} не найден. Создан пустой файл.")
        return {}

    df = pd.read_csv(SYMBOLS_FILE)

    if df.empty:
        logging.warning(f"Файл {SYMBOLS_FILE} пуст. Используется пустой symbols_id.")
        return {}

    symbols_dict = dict(zip(df['symbol'], df['u_id']))
    logging.info(f"Загружено {len(symbols_dict)} записей из {SYMBOLS_FILE}.")
    return symbols_dict


# --- Функции работы с датами ---
def get_transact_time():
    """Возвращает текущее UTC-время в формате 'YYYY-MM-DDTHH:MM:SSZ'."""
    return datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

def get_trade_date():
    """Возвращает текущую UTC-дату в формате 'YYYY-MM-DD'."""
    return datetime.datetime.utcnow().strftime('%Y-%m-%d')

# --- Функция получения баланса аккаунта ---
def get_balance(account_id) -> int:
    """Получает баланс аккаунта по API."""
    url = f'https://rest.portal.stage.unityfinance.net/api/v1/accountBalance?accountId={account_id}'
    response = requests.get(url, headers={'accept': 'application/json', 'auth-token': TOKEN}).json()
    return response['assetBalance'][0]['amount']

# --- Функция обновления trade_bd.csv ---
def update_trade_file(df: pd.DataFrame, file_path="trade_bd.csv") -> pd.DataFrame:
    """Обновляет trade_bd.csv, добавляя новые уникальные ордера."""
    if not os.path.exists(file_path):
        df.to_csv(file_path, index=False)
        logging.info(f"Создан новый файл {file_path} с {len(df)} записями.")
        return df

    existing_df = pd.read_csv(file_path)
    existing_order_ids = existing_df['orderId'].tolist()
    unique_df = df[~df['orderId'].isin(existing_order_ids)]

    if unique_df.empty:
        logging.info("Новых ордеров для записи нет.")
        return pd.DataFrame()

    unique_df.to_csv(file_path, mode='a', header=False, index=False)
    logging.info(f"Добавлено {len(unique_df)} новых ордеров в {file_path}.")
    return unique_df

# --- Функция получения истории ордеров ---
def get_order_history():
    session = HTTP(
    testnet=False,
    api_key="rixIdgl13et1dCa8pX",
    api_secret="Dvy76elR0ZAFjklSUhPfqpnjzAFlxPSRCLTR",
)
    """Получает историю ордеров и передает их в обработку."""
    logging.info("Запрос истории ордеров...")
    data = session.get_order_history(category="linear", limit=5)
    df = pd.DataFrame(data['result']['list'][::-1])
    df = df[['symbol', 'orderId', 'qty', 'side', 'price', 'updatedTime']]
    
    df = update_trade_file(df)
   
    
    if not df.empty:
        for _, row in df.iterrows():
            success = send_to_U(row['orderId'], row['symbol'], row['side'], row['qty'], float(row['price']))
            if not success:
                save_unsend_symbols(row)

# --- Функция отправки данных в API ---
def send_to_U(orderId: str, symbol: str, side: str, qty: str, price: float):
    """Отправляет ордер в API для всех аккаунтов."""
    url = 'https://rest.portal.stage.unityfinance.net/api/v1/addDirectTrade'
    headers = {'auth-token': TOKEN, 'Content-Type': 'application/json'}

    if symbol not in symbols_id:
        logging.error(f"❌ Символ {symbol} не найден в базе.")
        send_telegram_message(f"❌ Символ {symbol} не найден в базе.")
        return False  # Выходим сразу, если символа нет

    total_balance = sum(get_balance(acc) for acc in accaunts)
    account_ratios = {acc: get_balance(acc) / total_balance for acc in accaunts}

    success = True  # Флаг успешности всех отправок

    for clientAccountId, ratio in account_ratios.items():
        amount = round(float(qty) * float(ratio), 4)
        message = {
            "providerAccountId": 2300,
            "clientAccountId": clientAccountId,
            "instrumentId": symbols_id[symbol], 
            "side": side.upper(),
            "amount": amount,
            "price": price,
            "commission": 0,
            "transactTime": get_transact_time(),
            "tradeDate": get_trade_date(),
            "valueDate": get_trade_date(),
            "orderId": str(orderId),
            "comment": "",
            "mustBeSendToFix": False,
            "skipMarginCheck": False,
            "useExternalCommission": False,
            "clientCloseTradeId": "4"
        }
        
        response = requests.post(url, json=message, headers=headers)

        if response.status_code == 200:
            logging.info(f"✅ Ордер {symbol} отправлен успешно для аккаунта {clientAccountId}.")
            send_telegram_message(f"✅ Ордер {symbol} отправлен успешно для аккаунта {clientAccountId}.")
        else:
            logging.warning(f"⚠ Ошибка при отправке ордера {symbol} для аккаунта {clientAccountId}: {response.status_code}")
            send_telegram_message(f"⚠ Ошибка при отправке ордера {symbol} для аккаунта {clientAccountId}: {response.status_code}")
            success = False  # Если хотя бы одна отправка не удалась, меняем флаг

    return success  # Возвращаем True, если ВСЕ ордера успешно отправлены, иначе False


# --- Функция сохранения неотправленных ордеров ---
def save_unsend_symbols(row: pd.Series):
    """Сохраняет неотправленные ордера в файл unsend_symbols.csv."""
    file_path = 'unsend_symbols.csv'
    if not os.path.exists(file_path):
        pd.DataFrame(columns=["symbol", "orderId", "qty", "side", "price", "updatedTime", "Send_to_U"]).to_csv(file_path, index=False)
    
    df = pd.DataFrame([row])
    df.to_csv(file_path, mode='a', header=False, index=False)
    logging.warning(f"Ордер {row['symbol']} - {row['orderId']} не отправлен. Записан в {file_path}.")
    send_telegram_message(f"Ордер {row['symbol']} - {row['orderId']} не отправлен. Записан в {file_path}.")


# --- Функция для отправки неотправленных ордеров ---
def send_unsended_orders():
    file_path = 'unsend_symbols.csv'

    if not os.path.exists(file_path):
        logging.info("Файл unsend_symbols.csv не найден.")
        send_telegram_message("Нет неотправленных ордеров.")
        return
    
    df = pd.read_csv(file_path)
    if df.empty:
        logging.info("Нет неотправленных ордеров.")
        send_telegram_message("Нет неотправленных ордеров.")
        return
    
    remaining_orders = pd.DataFrame(columns=df.columns)
    for _, row in df.iterrows():
        success = send_to_U(row['orderId'], row['symbol'], row['side'], row['qty'], float(row['price']))
        if not success:
            remaining_orders = pd.concat([remaining_orders, pd.DataFrame([row])], ignore_index=True)

    if not remaining_orders.empty:
        remaining_orders.to_csv(file_path, index=False)
        logging.warning(f"{len(remaining_orders)} ордеров осталось в {file_path}.")
        send_telegram_message(f"{len(remaining_orders)} ордеров осталось в {file_path}.")
    else:
        os.remove(file_path)
        logging.info("Все неотправленные ордера успешно отправлены. Файл удален.")
        send_telegram_message("Все неотправленные ордера успешно отправлены. Файл удален.")
    

# --- Основной вызов программы ---
def main():
    logging.info("Запуск получения истории ордеров...")
    global symbols_id  # Делаем переменную глобальной
    symbols_id = load_symbols_id()  # Загружаем актуальный словарь
    get_order_history()
    logging.info("Процесс завершен.")

# if __name__ == "__main__":
#     main()
