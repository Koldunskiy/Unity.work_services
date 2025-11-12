
from datetime import datetime, timedelta
from binance.client import Client
import requests
import time
import hmac
import hashlib
from typing import List, Dict, Optional
from log.logger import get_logger
logger = get_logger(__file__)



def get_week_range_ms(n_weeks_ago: int):
    """
    Возвращает диапазон времени длиной 7 дней, заканчивающийся n_weeks_ago недель назад от текущего момента.

    Параметры:
        n_weeks_ago (int): Сколько недель назад должен заканчиваться диапазон.
                           Например, 0 — текущая неделя (последние 7 дней до сейчас),
                           1 — неделя перед текущей (от -14 до -7 дней от сейчас),
                           2 — две недели назад (от -21 до -14 дней от сейчас).

    Возвращает:
        tuple: (start_time_ms, end_time_ms) — временные метки в миллисекундах.
    """
    if n_weeks_ago < 0:
        raise ValueError("n_weeks_ago must be non-negative")

    ms_per_day = 24 * 60 * 60 * 1000
    ms_per_week = 7 * ms_per_day

    now_ms = int(time.time() * 1000)
    end_time_ms = now_ms - n_weeks_ago * ms_per_week
    start_time_ms = end_time_ms - ms_per_week

    return start_time_ms, end_time_ms

class HistTrades:
    try:
        def __init__(self, api_key, secret_key):
            self.api_key = api_key
            self.secret_key = secret_key
            self.client = Client(api_key, secret_key)

        def spot_hist_trades(self, symbol: str, limit: int = 1000):

            end_time = datetime.now()  # Текущая дата и время
            start_time = end_time - timedelta(days=1)  

            # Конвертация в миллисекунды (Unix timestamp)
            startTime = int(start_time.timestamp() * 1000)
            endTime = int(end_time.timestamp() * 1000)

            return self.client.get_my_trades(
                        symbol=symbol,
                        startTime=startTime,
                        endTime=endTime,
                        limit=limit
                    )

            
        def future_hist_trades(self, symbol: str, limit: int = 1000):
            end_time = datetime.now()  # Текущая дата и время
            start_time = end_time - timedelta(days=6)  

            # Конвертация в миллисекунды (Unix timestamp)
            startTime = int(start_time.timestamp() * 1000)
            endTime = int(end_time.timestamp() * 1000)

            return self.client.futures_account_trades(
                        symbol=symbol,
                        startTime=startTime,
                        endTime=endTime,
                        limit=limit
                    )
        
        def margin_hist_trade(self, symbol: str, startTime: str = None, endTime: str = None,  limit: int = 1000):
            
            if startTime == None:
                end_time = datetime.now()  # Текущая дата и время
                start_time = end_time - timedelta(days=1)  

                # Конвертация в миллисекунды (Unix timestamp)
                startTime = int(start_time.timestamp() * 1000)
                endTime = int(end_time.timestamp() * 1000)

            return self.client.get_margin_trades(
                        symbol=symbol,
                        startTime=startTime,
                        endTime=endTime,
                        limit=limit
                    )
        
        def get_sell_margin_trades(self, 
                    symbol: str,
                    startTime: str = None, 
                    endTime: str = None,
                    limit: int = 1000
                ) -> List[Dict]:
            
            if startTime == None:
                end_time = datetime.now()  # Текущая дата и время
                start_time = end_time - timedelta(days=6)  

                # Конвертация в миллисекунды (Unix timestamp)
                startTime = int(start_time.timestamp() * 1000)
                endTime = int(end_time.timestamp() * 1000)
     
            # Параметры запроса
            params = {
                'symbol': symbol.upper(),
                'startTime': startTime,
                'endTime': endTime,
                'limit': limit,  
                'timestamp': int(time.time() * 1000)
            }

            # Формируем строку для подписи
            query_string = '&'.join(f"{k}={v}" for k, v in params.items())
            signature = hmac.new(
                self.secret_key.encode('utf-8'),
                query_string.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()

            # URL и заголовки
            url = "https://papi.binance.com/papi/v1/um/userTrades"
            headers = {'X-MBX-APIKEY': self.api_key}

            # Выполняем запрос
            try:
                response = requests.get(
                    url,
                    params={**params, 'signature': signature},
                    headers=headers,
                    timeout=10
                )
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                logger.error(f"Ошибка при запросе к Binance API: {e}")
                if response is not None:
                    logger.error("Ответ сервера:", response.text)
                return []

    except Exception as e:
        logger.error(f'Ошибка: {e}')