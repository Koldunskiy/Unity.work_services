import sqlite3
import json
from datetime import datetime
import pytz
import os
from utilites import send_trade_to_unity
from config import INSTRUMENT_IDS
from log.logger import get_logger

logger = get_logger(__file__)

class TradeDatabase:
    def __init__(self, CONFIG: dict, trader_name: str):
        self.db_path = 'trades.db'
        self.trader_name = trader_name
        self.table_name = f"trades_{trader_name}"  # Уникальное имя таблицы для трейдера
        
        # Нормализуем CONFIG
        if isinstance(CONFIG, dict) and trader_name in CONFIG:
            self.config = CONFIG[trader_name]
        else:
            self.config = CONFIG or {}
        
        # Проверяем и создаем таблицу если нужно
        self.check_and_create_table()
    
    def check_and_create_table(self):
        """Проверяет существование таблицы и создает если её нет"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Проверяем существует ли таблица
        cursor.execute(f"""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name=?
        """, (self.table_name,))
        
        table_exists = cursor.fetchone() is not None
        
        if not table_exists:
            self.create_table(conn, cursor)
        
        conn.close()
    
    def create_table(self, conn, cursor: sqlite3.Cursor):
        """Создание таблицы для конкретного трейдера"""
        cursor.execute(f'''
            CREATE TABLE {self.table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ordId TEXT NOT NULL,
                tradeId TEXT NOT NULL,
                instId TEXT NOT NULL,
                side TEXT NOT NULL,
                avgPx REAL,
                state TEXT NOT NULL,
                uTime BIGINT,
                fillSz REAL,
                is_send BOOLEAN DEFAULT FALSE,
                created_at DATETIME DEFAULT (datetime('now', 'localtime')),
                ordType TEXT,
                commission REAL DEFAULT 0
            )
        ''')
        
        # Создаем индексы
        cursor.execute(f'CREATE INDEX IF NOT EXISTS idx_ordId ON {self.table_name}(ordId)')
        cursor.execute(f'CREATE INDEX IF NOT EXISTS idx_instId ON {self.table_name}(instId)')
        cursor.execute(f'CREATE INDEX IF NOT EXISTS idx_side ON {self.table_name}(side)')
        cursor.execute(f'CREATE INDEX IF NOT EXISTS idx_state ON {self.table_name}(state)')
        cursor.execute(f'CREATE INDEX IF NOT EXISTS idx_created_at ON {self.table_name}(created_at)')
        
        conn.commit()
        conn.close()
    

    def sync_trades_from_list(self, trades):
        """
        Принять список сделок (словарей), проверить по tradeId наличие в БД,
        и вставить только те, которых нет.
        Возвращает статистику {'inserted': N, 'skipped': M, 'errors': K}
        """
        inserted = 0
        skipped = 0
        errors = 0

        if not trades:
            logger.info(f"Пустой список сделок для синхронизации {self.trader_name}")
            return {'inserted': 0, 'skipped': 0, 'errors': 0}

        logger.info(f"Получено {len(trades)} сделок для синхронизации для {self.trader_name}")

        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.cursor()
            for t in trades:
                try:
                    trade_id = t.get('tradeId')
                    if not trade_id:
                        errors += 1
                        continue
                    
                    # Проверяем наличие по tradeId
                    cursor.execute(f'SELECT 1 FROM {self.table_name} WHERE tradeId = ? LIMIT 1', (trade_id,))
                    exists = cursor.fetchone() is not None
                    if exists:
                        skipped += 1
                        continue

                    # Нормализуем поля и вставляем ровно под вашу схему
                    cursor.execute(f'''
                        INSERT INTO {self.table_name} (
                            ordId, tradeId, instId, side, avgPx, state, uTime, fillSz, ordType, commission
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        t.get('ordId'),
                        t.get('tradeId'),
                        t.get('instId'),
                        t.get('side'),
                        float(t.get('avgPx', t.get('fillPx')) or 0),
                        t.get('state', 'filled'),
                        int(t.get('uTime', t.get("ts")) or 0),
                        float(t.get('fillSz', 0) or 0),
                        t.get('ordType'),
                        t['fee']
                    ))
                    inserted += 1
                except Exception:
                    errors += 1

            conn.commit()
        finally:
            conn.close()

        return {'inserted': inserted, 'skipped': skipped, 'errors': errors}


    def aggregate_and_send_unsent(self):
        """
        Отправить все неотправленные сделки по одной, без агрегации.
        Каждая запись из БД отправляется отдельно через send_trade_to_unity.
        """
        logger.info("Сканирование базы данных на неотправленные сделки")
        flag = False
        
        try:
            # Первое подключение - только для чтения
            with sqlite3.connect(self.db_path) as read_conn:
                read_conn.row_factory = sqlite3.Row
                read_cursor = read_conn.cursor()
                
          

                read_cursor.execute(
                    f'SELECT * FROM {self.table_name} WHERE is_send = FALSE ORDER BY created_at desc limit 1000'   # 10000!
                )
                rows = read_cursor.fetchall()

            sent = 0
            failed = 0

            for row in rows:
                ordId = row['ordId']
                tradeId = row['tradeId']
                inst_id = row['instId']
                side = row['side']
                qty = float(row['fillSz'] or 0)
                px = float(row['avgPx'] or 0)
                ts = row['uTime']
                commission = 0 if row['commission'] < 0 else row['commission']


                # logger.info(
                #     "Отправка сделки: ordId=%s, инструмент=%s, сторона=%s, объём=%s, цена=%s",
                #     ordId, inst_id, side, qty, px
                # )

                status = send_trade_to_unity(
                    providerAccountId=self.config.get('providerAccountId'),
                    clientAccountId=self.config.get('clientAccountId'),
                    instrumentId=INSTRUMENT_IDS.get(inst_id),
                    side=side,
                    amount=qty,
                    price=px,
                    comment=f"{self.trader_name}_{ordId}",
                    timestamp=ts,
                    orderId=tradeId,
                    commission=commission
                )
                
                # print(f"Status code: {status.status_code}")
                
                # Отдельное подключение для каждого UPDATE
                try:
                    with sqlite3.connect(self.db_path) as update_conn:
                        update_cursor = update_conn.cursor()
                        
                        if status.status_code == 200:
                            update_cursor.execute(
                                f'UPDATE {self.table_name} SET is_send = TRUE WHERE ordId = ? AND tradeId = ?', 
                                (ordId, tradeId)
                            )
                            update_conn.commit()
                            sent += 1
                            logger.info("Запись с ordId=%s и tradeId=%s помечена как отправленная, 200", ordId, tradeId)
                        else:
                            failed += 1
                            logger.warning(
                                "Не удалось отправить запись ordId=%s, tradeId=%s. статус=%s, текст=%s", 
                                ordId, tradeId, status.status_code, status.text
                            )
                            
                except sqlite3.Error as e:
                    logger.error("Ошибка при обновлении БД для ordId=%s: %s", ordId, e)
                    failed += 1

                # Интерактивное управление
                if flag:
                    print('1 - ручное управление, 2 - автомат, 0 - остановить.')
                    try:
                        a = int(input())
                        if a == 0:
                            return {'records': len(rows), 'sent': sent, 'failed': failed}
                        if a == 2:
                            flag = False
                    except ValueError:
                        print("Некорректный ввод, продолжаем автоматически")
                        flag = False

        except sqlite3.Error as e:
            logger.error("Ошибка при работе с БД: %s", e)
            return {'records': 0, 'sent': 0, 'failed': 0}

        return {'records': len(rows), 'sent': sent, 'failed': failed}







# from config import CONFIG_DICT_TEST

# from historical_trades import OkxFillsFetcher

# db = TradeDatabase(CONFIG=CONFIG_DICT_TEST, trader_name="TEST")
# print(db.aggregate_and_send_unsent())


# fetcher = OkxFillsFetcher(
#     api_key="f5b2fe81-df67-42b2-8151-6580a4a3242a",
#     api_secret="3DF508E92CAF5C51EEC4BD9D8FCAE389",
#     passphrase="STP230125test!",
#     base_url="https://www.okx.com",   # можно оставить по умолчанию
#     simulated=False                   # True, если используешь demo-режим
# )

# # Забираем сделки за 7 дней (по умолчанию)
# fills = fetcher.fetch_days(2)
# print(fills)



# print(db.sync_trades_from_list(fills))


# # Пример использования
# if __name__ == "__main__":
#     # Создаем базу данных
#     db = TradeDatabase()
#     db.aggregate_and_send_unsent()
    
    # # Пример данных из вашего JSON
    # trade_data = {
    #     'instType': 'SWAP',
    #     'instId': 'BTC-USDT-SWAP',
    #     'ordId': '2834757289781092353',
    #     'tradeId': '1738367414',
    #     'side': 'buy',
    #     'avgPx': '110606.6',
    #     'state': 'filled',
    #     'uTime': '1756984750641',
    #     'fillSz': '0.01',
    #     'ordType': 'market'
    # }
    
    # # Вставляем данные
    # success = db.insert_trade(trade_data)
    # print(f"Данные добавлены: {success}")
    
    