import sqlite3
import json
from datetime import datetime
import pytz
import os
from utilites import send_trade_to_unity
from config import INSTRUMENT_IDS
from log.logger import get_logger
import asyncio
import aiohttp
from tqdm.asyncio import tqdm  # для асинхронного tqdm


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
    

    def sync_trades_from_list(self, trades, instrument=None):
        """
        Принять список сделок (словарей), проверить по tradeId наличие в БД,
        и вставить только те, которых нет.
        Возвращает статистику {'inserted': N, 'skipped': M, 'errors': K}
        
        Args:
            trades: список сделок (спот или фьючерсы)
            instrument: инструмент (например, 'btcusdt') для случаев, когда его нет в данных
        """
        inserted = 0
        skipped = 0
        errors = 0

        if not trades:
            # logger.info("Пустой список сделок для синхронизации")
            return {'inserted': 0, 'skipped': 0, 'errors': 0}

        logger.info("Получено %d сделок для синхронизации", len(trades))

        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.cursor()
            for t in trades:
                try:
                    # Определяем trade_id в зависимости от структуры данных
                    trade_id = t.get('id')
                    if not trade_id:
                        errors += 1
                        continue
                    
                    # Проверяем наличие по tradeId
                    cursor.execute(f'SELECT 1 FROM {self.table_name} WHERE tradeId = ? LIMIT 1', (trade_id,))
                    exists = cursor.fetchone() is not None
                    if exists:
                        skipped += 1
                        continue

                    
                    order_id = t.get('orderId')
                    inst_id = t.get('symbol', instrument)
                    side = t.get('side', 'buy' if t.get('isBuyer', False) else 'sell')
                    avg_px = float(t.get('price', 0)) if t.get('price') else 0
                    fill_sz = float(t.get('qty', 0)) if t.get('qty') else 0
                    time_field = t.get('time', 0)
                    comission = t.get('commission', 0)
                    
                    # Вставляем данные в базу
                    cursor.execute(f'''
                        INSERT INTO {self.table_name} (
                            ordId, tradeId, instId, side, avgPx, state, uTime, fillSz, ordType, commission
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        order_id,
                        trade_id,
                        inst_id,
                        side,
                        avg_px,
                        'filled',  # state по умолчанию
                        int(time_field),
                        fill_sz,
                        'market',  # ordType по умолчанию
                        comission
                    ))
                    inserted += 1
                    
                except Exception as e:
                    logger.error(f"Ошибка при обработке сделки {t}: {e}")
                    errors += 1

            conn.commit()
        finally:
            conn.close()

        logger.info("Синхронизация завершена: inserted=%d, skipped=%d, errors=%d", 
                    inserted, skipped, errors)
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
                
                # read_cursor.execute(
                #     'SELECT * FROM trades_Steven_Binanc WHERE is_send = FALSE ORDER BY created_at desc limit 2'
                # )

                read_cursor.execute(
                    f'SELECT * FROM {self.table_name} WHERE is_send = FALSE ORDER BY created_at desc limit 2000'
                )
                rows = read_cursor.fetchall()

            sent = 0
            failed = 0

            for row in tqdm(rows, desc="Processing rows"):
                ordId = row['ordId']
                tradeId = row['tradeId']
                inst_id = row['instId']
                side = row['side']
                qty = float(row['fillSz'] or 0)
                px = float(row['avgPx'] or 0)
                ts = row['uTime']
                commission = row['commission']


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
                
                print(f"Status code: {status.status_code}")
                
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



