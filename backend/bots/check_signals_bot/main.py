import requests
import pandas as pd
import sqlite3
import re
import schedule
import time
from dop_file import main_fun

d = {1686: 'BTCUSDT',
 1690: 'ETHUSDT',
 2189: 'DOGEUSDT',
 1692: 'LTCUSDT',
 1698: 'ADAUSDT',
 2209: 'SOLUSDT'}


def extract_trading_levels(text):
    # Шаблоны для поиска входа, целей и стоп-лосса
    patterns = {
        'entry': re.compile(r'\b(?:Вход|Entry):\s*(\d+\.\d+)'),
        'tp1': re.compile(r'\b(?:Первая цель|TP1):\s*(\d+\.\d+)'),
        'tp2': re.compile(r'\b(?:Вторая цель|TP2):\s*(\d+\.\d+)'),
        'sl': re.compile(r'\b(?:Стоп-ордер|SL):\s*(\d+\.\d+)')
    }

    # Результаты поиска
    levels = {}
    for key, pattern in patterns.items():
        match = pattern.search(text)
        levels[key] = float(match.group(1)) if match else None

    return levels


def download_signals():
    
    url = "https://clientapi.bondah.com/articles"
    headers = {
        "LanguageId": "7" 
    }
    for id_symbols in d.keys():
        params = {
            "FromId": None,           
            "ArticlesCount": 4,      # Количество статей (по умолчанию 10)
            "InstrumentId": id_symbols,
            "IsSignals": True
        }
        # Выполнение GET-запроса
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()  # Проверка на успешность запроса
            articles = response.json()  # Декодирование ответа в JSON
            # print(articles)
        except requests.exceptions.RequestException as e:
            print("Ошибка выполнения запроса:", e)
            raise e
        
        df = pd.DataFrame(articles)
        df['createTime'] = pd.to_datetime(df['createTime'])
        df.drop(['analyseTypeId', 'snapshotId', 'timeAgo', 'mtPicture'], axis=1, inplace=True)
        df[['entry', 'tp1', 'tp2', 'sl']] = df['body'].apply(lambda x: pd.Series(extract_trading_levels(x)))
        df['instrumentId'] = df['instrumentId'].replace(d)
        df['createTime'] = df['createTime'].astype(str)
        df['is_check'] = 0
        conn = sqlite3.connect('trading_analysis.db')
    
        # Функция для проверки существования записи

        def record_exists(cursor, record_id):
            cursor.execute("SELECT COUNT(*) FROM Trade_Signals WHERE id = ?", (record_id,))
            return cursor.fetchone()[0] > 0

        # Вставка данных из DataFrame с проверкой
        cursor = conn.cursor()
        for index, row in df.iterrows():
            if not record_exists(cursor, row['id']):  # Проверяем, существует ли запись
                cursor.execute('''
                INSERT INTO Trade_Signals (
                    id, instrumentId, analyseType, header, body, createTime, foreCast, entry, tp1, tp2, sl, is_check
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    row['id'], row['instrumentId'], row['analyseType'], row['header'], row['body'],
                    row['createTime'], row['foreCast'], row['entry'], row['tp1'], row['tp2'], row['sl'], row['is_check']
                ))
 
        # Сохранение изменений и закрытие соединения
        conn.commit()
        conn.close()




if __name__ == "__main__":
    print('import and checking signal api patterns started!')
    while True:
        
        download_signals()
        main_fun()
        time.sleep(60 * 60 * 24)