import requests
import pandas as pd
import re
from datetime import datetime, timedelta
import json
import time
import random 
# Словарь соответствий инструментов
df_id = pd.read_csv('id_instruments_prod.csv')
id_unity = df_id['id_unity'].astype(int).tolist()
id_bondash = df_id['id_bondash'].astype(int).tolist()
ticket = df_id["Ticket"].tolist()
reaL_value = dict(zip(id_bondash, id_unity))
id_trans_to_ticket = dict(zip(id_bondash, ticket))
find_instr = dict(zip(id_unity, ticket))
# reaL_value = {1: 47, 1686: 61343, 191: 8115, 250: 1291, 238: 4711}


TOKEN = '6766212755:AAGNwQDGrFoICY4s3WwHLBY0tH55AY6U01c'
URL = 'https://api.telegram.org/bot'
chat_id = -4017930976


def send_message(text:str):
    requests.get('https://api.telegram.org/bot{}/sendMessage'.format(TOKEN),
                       params={'chat_id': chat_id, 'text': text})
    


# URL и токен для запросов
url = 'https://rest.unity.finance/api/v1/createTradeIdea'
token = '666beb18-942a-46e9-87d7-e327905d6219' # prod U

headers = {
    "accept": "application/json",
    "auth-token": token,
    'Content-Type': 'application/json; charset=utf-8'
}

# Логирование
log_file = "logfile.log"
def log_message(message):
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

# def translane(text) ->str:
#     base_url = "https://ftapi.pythonanywhere.com/translate"

#     params = {
#         "sl": "ru",  # Исходный язык (русский)
#         "dl": "en",  # Целевой язык (английский)
#         "text": text # Текст для перевода
#     }

#     # Выполнение GET-запроса
#     response = requests.get(base_url, params=params)

#     # Проверка статуса ответа
#     if response.status_code == 200:
#         translation_data = response.json()
#         return  translation_data["destination-text"]
#     else:
#         log_message('Ошибка в переводе. Не удалось перевести текст')
#         return " "


# Функция для преобразования времени
def make_correct_time(time: str, delta: int = 0) -> str:
    date_obj = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
    date_obj += timedelta(hours=delta)
    return date_obj.strftime('%Y-%m-%dT%H:%M:%SZ')




def extract_trading_levels_from_escaped(escaped_text: str):
    """
    Извлекает торговые уровни из экранированного текста.
    Допускается наличие пробельных символов и экранированных последовательностей (например, "\\n")
    между ключевыми словами и значениями.
    """
    # Разрешаем пробелы и последовательности "\n"
    sep = r'(?:\s|\\n)*'
    patterns = {
        'entry': re.compile(r'\b(?:Вход|Entry):' + sep + r'(\d+\.\d+)'),
        'tp1': re.compile(r'\b(?:Первая цель|TP1):' + sep + r'(\d+\.\d+)'),
        'tp2': re.compile(r'\b(?:Вторая цель|TP2):' + sep + r'(\d+\.\d+)'),
        'sl': re.compile(r'\b(?:Стоп-ордер|SL):' + sep + r'(\d+\.\d+)')
    }
    
    levels = {}
    for key, pattern in patterns.items():
        match = pattern.search(escaped_text)
        levels[key] = float(match.group(1)) if match else None
    return levels



# Получение данных
def get_data() -> list[list]:
    bondah_url = "https://clientapi.bondah.com/articles"
    headers = {"LanguageId": "7"}
    params = {
        "FromId": None,
        "ArticlesCount": 10,
        "InstrumentId": reaL_value.keys(),
        "IsSignals": True
    }
    languages = [7, 1]  # RU и EN или другие идентификаторы языков

    # Хранилище для результатов
    all_articles = []

    # Выполнение запросов для каждого языка
    for lang in languages:
        headers = {"LanguageId": str(lang)}
        try:
            response = requests.get(bondah_url, headers=headers, params=params)
            response.raise_for_status()  # Проверка на успешность запроса
            articles = response.json()  # Декодирование ответа в JSON
            all_articles.append(articles)  # Добавляем результаты в общий список
        except requests.exceptions.RequestException as e:
            log_message(f"Ошибка выполнения запроса для языка {lang}:", e)
            return []
    return all_articles



# Обработка данных
def process_data(all_articles: list):
    if not all_articles:
        log_message("Нет новых данных для обработки.")
        return
    
    ru_df = pd.DataFrame(all_articles[0])
    en_df = pd.DataFrame(all_articles[1])
    ru_df['header_en'] = en_df['header'].copy()
    ru_df['body_en'] = en_df['body'].copy()
    df = ru_df.copy()

    df['createTime'] = pd.to_datetime(df['createTime'])
    df.drop(['analyseTypeId', 'snapshotId', 'timeAgo', 'mtPicture'], axis=1, inplace=True, errors='ignore')

    df_id = pd.read_csv('check_id.csv')
    new_df = df[df.id > df_id.id[0]].copy()
    if new_df.empty:
        log_message("Нет новых записей для обработки.")
        return

    df_id.id = df.id.max()
    df_id.to_csv('check_id.csv', index=False)

    new_df[['entry', 'tp1', 'tp2', 'sl']] = new_df['body'].apply(lambda x: pd.Series(extract_trading_levels_from_escaped(x)))
    new_df['instrumentId'] = new_df['instrumentId'].replace(reaL_value)
    new_df['createTime'] = new_df['createTime'].astype(str)
    new_df['foreCast'] = new_df['foreCast'].replace({'Down': 'SELL', 'Up': 'BUY'})
    new_df['expirationTime'] = new_df['createTime'].apply(lambda x: make_correct_time(time=x, delta=24))
    new_df['createTime'] = new_df['createTime'].apply(lambda x: make_correct_time(x))

    for index, row in new_df.iterrows():
        print(row)
        en_header = row['header_en']
        en_body = row['body_en']
        target = {
            "instrumentIds": [row['instrumentId']],
            "openOrderType": "LIMIT",
            "side": "BUY",
            "price": row['entry'],
            "stopLoss": row['sl'],
            "takeProfit": row['tp1'],
            "confidence": f'{random.randint(55, 90) / 100}',
            "expirationTime": row['expirationTime'],
            "localeDescriptions": [
               {
                "locale": "RU",
                "target": (row['header']),
                "background": (row['body']).replace('<br/>', '\n')
            },
            {
                "locale": "EN",
                "target": (en_header),
                "background": (en_body).replace('<br/>', '\n')
            }
            ],
            "status": "ACTIVE",
            "publishTime": row['createTime'],
            "source": "Bondah Analytics",
            "provider": "UNITY",
            "state": "LIVE_TRADE",
            "externalId": str(row['id']),
            "subscribers": 0,
            "priority": 0,
            "rate": 0,
            "confidence": f'{random.randint(55, 90) / 100}',
        }

        payload = json.dumps(target, indent=4, ensure_ascii=False)

        response = requests.post(url, headers=headers, data=payload.encode('utf-8'))


        if response.status_code == 200:
            log_message(f"Успешно отправлено: {find_instr[row['instrumentId']], row['id']}")
            send_message(f"Успешно отправлено: {find_instr[row['instrumentId']], row['id']}")
        else:
            log_message(f"Ошибка отправки: {find_instr[row['instrumentId']], row['id']}, Код: {response.status_code}, Ответ: {response.text}")
            send_message(f"Ошибка отправки: {find_instr[row['instrumentId']], row['instrumentId']}, Код: {response.status_code}, Ответ: {response.text}")

# Планировщик выполнения
if __name__ == "__main__":
    print("Скрипт для передачи сигналов из Bonash в  Unity заработал")
    while True:
        current_time = datetime.now()
        if current_time.minute in [2]:
            log_message("Начало обработки данных.")
            try:
                data = get_data()
                process_data(data)
            except Exception as e:
                log_message(f"Ошибка в процессе выполнения: {e}")
            log_message("Обработка завершена.")

            # Ожидание до следующей минуты для предотвращения повторного выполнения
            time.sleep(60 - datetime.now().second)
        else:
            # Ожидание до следующей проверки минуты
            time.sleep(10)
