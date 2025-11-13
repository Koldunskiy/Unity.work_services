import requests
import pandas as pd
import sqlite3
import re
import schedule
import time
from dop_file import main_fun

# Словарь соответствия ID → символ
INSTRUMENT_MAP = {
    1686: 'BTCUSDT',
    1690: 'ETHUSDT',
    2189: 'DOGEUSDT',
    1692: 'LTCUSDT',
    1698: 'ADAUSDT',
    2209: 'SOLUSDT'
}


def extract_trading_levels(text: str) -> dict:
    """Извлекает уровни входа, TP1, TP2 и SL из текста сигнала.

    Args:
        text (str): Текст сигнала.

    Returns:
        dict: Словарь с ключами: 'entry', 'tp1', 'tp2', 'sl' (float или None).
    """
    patterns = {
        'entry': re.compile(r'\b(?:Вход|Entry):\s*(\d+\.\d+)'),
        'tp1': re.compile(r'\b(?:Первая цель|TP1):\s*(\d+\.\d+)'),
        'tp2': re.compile(r'\b(?:Вторая цель|TP2):\s*(\d+\.\d+)'),
        'sl': re.compile(r'\b(?:Стоп-ордер|SL):\s*(\d+\.\d+)')
    }

    levels = {}
    for key, pattern in patterns.items():
        match = pattern.search(text)
        levels[key] = float(match.group(1)) if match else None

    return levels


def download_signals() -> None:
    """Скачивает сигналы с API Bondah и сохраняет в БД (если новых)."""
    url = "https://clientapi.bondah.com/articles"
    headers = {"LanguageId": "7"}

    for instrument_id, symbol in INSTRUMENT_MAP.items():
        params = {
            "FromId": None,
            "ArticlesCount": 4,
            "InstrumentId": instrument_id,
            "IsSignals": True
        }

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            articles = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе для {symbol}: {e}")
            continue

        df = pd.DataFrame(articles)
        if df.empty:
            continue

        df['createTime'] = pd.to_datetime(df['createTime'])
        df.drop(['analyseTypeId', 'snapshotId', 'timeAgo', 'mtPicture'], axis=1, inplace=True)

        # Извлекаем уровни
        df[['entry', 'tp1', 'tp2', 'sl']] = df['body'].apply(
            lambda x: pd.Series(extract_trading_levels(x))
        )

        df['instrumentId'] = symbol
        df['createTime'] = df['createTime'].astype(str)
        df['is_check'] = 0

        # === Сохранение в БД (только новые записи) ===
        conn = sqlite3.connect('trading_analysis.db')
        cursor = conn.cursor()

        for _, row in df.iterrows():
            cursor.execute("SELECT COUNT(*) FROM Trade_Signals WHERE id = ?", (row['id'],))
            if cursor.fetchone()[0] == 0:  # Записи нет
                cursor.execute('''
                    INSERT INTO Trade_Signals (
                        id, instrumentId, analyseType, header, body, createTime, 
                        foreCast, entry, tp1, tp2, sl, is_check
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    row['id'], row['instrumentId'], row['analyseType'], row['header'],
                    row['body'], row['createTime'], row['foreCast'], row['entry'],
                    row['tp1'], row['tp2'], row['sl'], row['is_check']
                ))

        conn.commit()
        conn.close()


if __name__ == "__main__":
    print('Запуск: импорт и проверка сигналов с API Bondah...')
    while True:
        download_signals()
        main_fun()
        print("Цикл завершён. Ожидание 24 часа...")
        time.sleep(60 * 60 * 24)