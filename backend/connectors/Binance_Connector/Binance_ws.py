import asyncio
import websockets
import json
import aiohttp
import time
import hmac
import hashlib
import urllib.parse
from datetime import datetime
from typing import Optional, Dict, Any
from log.logger import get_logger
from utilites import *
from config import INSTRUMENT_IDS


logging = get_logger(__file__)

class BinanceTradeMonitor:
    def __init__(self, api_key: str, secret_key: str, trader_name: str, providerAccountId: int, clientAccountId: int):
        self.api_key = api_key
        self.secret_key = secret_key
        self.trader_name = trader_name
        self.providerAccountId = providerAccountId
        self.clientAccountId = clientAccountId
        
        # Фьючерсные настройки
        self.future_base_url = "https://fapi.binance.com"
        self.future_ws_url = "wss://fstream.binance.com/ws"
        self.future_listen_key: Optional[str] = None
        self.future_websocket: Optional[websockets.WebSocketClientProtocol] = None
        
        # Спотовые настройки
        self.spot_base_url = "https://api.binance.com"
        self.spot_ws_url = "wss://stream.binance.com:9443/ws"
        self.spot_listen_key: Optional[str] = None
        self.spot_websocket: Optional[websockets.WebSocketClientProtocol] = None
        
        # Общие настройки
        self.reconnect_interval = 10 * 3600  # 10 часов (меньше 12 для надежности)
        self.keepalive_interval = 25 * 60   # 25 минут (меньше 30 для надежности)
        self.is_running = True

    def generate_signature(self, params: Dict[str, Any]) -> str:
        """Генерация подписи для запросов"""
        query_string = urllib.parse.urlencode(params)
        return hmac.new(
            self.secret_key.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

    async def get_future_listen_key(self) -> Optional[str]:
        """Получение listen key для фьючерсов"""
        endpoint = "/fapi/v1/listenKey"
        url = self.future_base_url + endpoint
        
        headers = {'X-MBX-APIKEY': self.api_key}
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    if response.status == 200:
                        data = await response.json()
                        self.future_listen_key = data['listenKey']
                        logging.info(f"✅ Получен фьючерсный listenKey: {self.future_listen_key[:15]}...")
                        return self.future_listen_key
                    else:
                        error_text = await response.text()
                        logging.error(f"❌ Ошибка получения фьючерсного listenKey: {error_text}")
                        return None
        except Exception as e:
            logging.error(f"❌ Исключение при получении фьючерсного listenKey: {e}")
            return None

    async def keepalive_future_listen_key(self) -> bool:
        """Продление срока действия фьючерсного listenKey"""
        if not self.future_listen_key:
            return False
            
        endpoint = "/fapi/v1/listenKey"
        url = self.future_base_url + endpoint
        
        headers = {'X-MBX-APIKEY': self.api_key}
        params = {'listenKey': self.future_listen_key}
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.put(url, headers=headers, params=params, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    if response.status == 200:
                        logging.debug("✅ Фьючерсный ListenKey успешно продлен")
                        return True
                    else:
                        error_text = await response.text()
                        logging.error(f"❌ Ошибка продления фьючерсного listenKey: {error_text}")
                        return False
        except Exception as e:
            logging.error(f"❌ Исключение при продлении фьючерсного listenKey: {e}")
            return False

    async def connect_future(self):
        """Подключение к фьючерсному WebSocket"""
        while self.is_running:
            try:
                # Получаем listenKey
                listen_key = await self.get_future_listen_key()
                if not listen_key:
                    logging.error("❌ Не удалось получить фьючерсный listenKey. Повторная попытка через 30 секунд...")
                    await asyncio.sleep(30)
                    continue
                
                # Формируем URL для подключения
                ws_url = f"{self.future_ws_url}/{listen_key}"
                
                logging.info("🔄 Попытка подключения к фьючерсному WebSocket...")
                
                # Подключаемся с правильными параметрами
                async with websockets.connect(
                    ws_url,
                    ping_interval=20,
                    ping_timeout=10,
                    close_timeout=10,
                    max_size=2**23  # 8MB buffer
                ) as websocket:
                    self.future_websocket = websocket
                    logging.info("✅ Успешное подключение к фьючерсному WebSocket Binance")
                    print(f"✅ Успешное подключение к фьючерсному WebSocket - {self.trader_name}")
                    
                    # Запускаем задачи
                    message_task = asyncio.create_task(self.handle_future_messages())
                    keepalive_task = asyncio.create_task(self.keepalive_future_loop())
                    reconnect_task = asyncio.create_task(self.schedule_future_reconnect())
                    
                    # Ожидаем завершения одной из задач
                    done, pending = await asyncio.wait(
                        [message_task, keepalive_task, reconnect_task],
                        return_when=asyncio.FIRST_COMPLETED
                    )
                    
                    # Отменяем оставшиеся задачи
                    for task in pending:
                        task.cancel()
                    
            except websockets.exceptions.ConnectionClosed as e:
                logging.error(f"❌ Фьючерсное соединение закрыто: {e}. Переподключение через 10 секунд...")
                await asyncio.sleep(10)
            except Exception as e:
                logging.error(f"❌ Ошибка соединения с фьючерсами: {e}. Переподключение через 10 секунд...")
                await asyncio.sleep(10)

    async def handle_future_messages(self):
        """Обработка сообщений от фьючерсного WebSocket"""
        try:
            async for message in self.future_websocket:
                try:
                    data = json.loads(message)
                    await self.process_future_message(data)
                except json.JSONDecodeError as e:
                    logging.error(f"❌ Ошибка декодирования JSON: {e}, сообщение: {message[:100]}")
                except Exception as e:
                    logging.error(f"❌ Ошибка обработки сообщения: {e}")
                    
        except websockets.exceptions.ConnectionClosed:
            logging.warning("⚠️ Фьючерсное соединение закрыто")
        except Exception as e:
            logging.error(f"❌ Ошибка в handle_future_messages: {e}")
            raise

    async def process_future_message(self, data: dict):
        """Обработка фьючерсных сообщений"""
        try:
            event_type = data.get('e', 'UNKNOWN')
            
            logging.info('full json F', data)
            # Логируем все важные события для отладки
            if event_type != 'UNKNOWN':
                logging.debug(f"📨 Фьючерсное событие {event_type}")
            
            # Обрабатываем событие исполнения ордера
            if data.get('e') == 'ORDER_TRADE_UPDATE':
                order_data = data['o']
                if order_data['x'] == 'TRADE':
                    self.log_future_trade(order_data, data['E'])
                    
            elif data.get('e') == 'ACCOUNT_UPDATE':
                logging.info("📊 Обновление фьючерсного аккаунта")
                
            elif data.get('e') == 'listenKeyExpired':
                logging.warning("⚠️ Фьючерсный listenKey истек, требуется переподключение")
                if self.future_websocket:
                    await self.future_websocket.close()
                    
        except Exception as e:
            logging.error(f"❌ Ошибка обработки фьючерсного сообщения: {e}")

    def log_future_trade(self, order_data: dict, event_time: int):
        """Логирование фьючерсной сделки"""
        try:
            
            trade_dict = {
            "ordId": order_data.get('i'),  # orderId из поля 'i'
            "tradeId": order_data.get('t'),  # tradeId из поля 't'
            "instId": order_data.get('s', 'UNKNOWN'),  # symbol из поля 's'
            "side": order_data.get('S', 'UNKNOWN'),  # приводим к нижнему регистру
            "avgPx": order_data.get('L', '0'),  # цена из поля 'L'
            "state": order_data.get('X', 'filled'),  # статус из поля 'X'
            "uTime": order_data.get('T', 0),  # время из поля 'T'
            "fillSz": order_data.get('l', '0'),  # количество из поля 'l'
            "ordType": order_data.get('o', 'MARKET')  # тип ордера из поля 'o'
            }
            

            resp = send_trade_to_unity(
                providerAccountId=self.providerAccountId,
                clientAccountId=self.clientAccountId,
                instrumentId=INSTRUMENT_IDS[order_data['s']],
                side=trade_dict['side'],
                amount=trade_dict['fillSz'],
                price=trade_dict['avgPx'],
                orderId=str(trade_dict['tradeId']),
                comment=self.trader_name)
            
            if resp.status_code == 200:
                logging.info(f'Сделка отправленна в Unity {trade_dict["tradeId"]}')
                is_send = True
            else:
                is_send = False
                logging.error(f"❌ Ошибка при отправке сделки :", resp.status_code, resp.text)

            insert_trade(trade_dict, self.trader_name, is_send)

        except Exception as e:
            logging.error(f"❌ Ошибка логирования фьючерсной сделки: {e}")

    async def keepalive_future_loop(self):
        """Цикл поддержания активности фьючерсного listenKey"""
        while self.is_running:
            await asyncio.sleep(self.keepalive_interval)
            if self.future_listen_key:
                success = await self.keepalive_future_listen_key()
                if not success:
                    logging.error("❌ Не удалось продлить фьючерсный listenKey. Инициирую переподключение...")
                    break

    async def schedule_future_reconnect(self):
        """Плановое переподключение для фьючерсов"""
        await asyncio.sleep(self.reconnect_interval)
        logging.info("🔄 Инициирование планового переподключения для фьючерсов")
        if self.future_websocket:
            await self.future_websocket.close()

    # СПОТОВЫЕ МЕТОДЫ
    async def get_spot_listen_key(self) -> Optional[str]:
        """Получение listen key для спота"""
        endpoint = "/api/v3/userDataStream"
        url = self.spot_base_url + endpoint
        
        headers = {'X-MBX-APIKEY': self.api_key}
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    if response.status == 200:
                        data = await response.json()
                        self.spot_listen_key = data['listenKey']
                        logging.info(f"✅ Получен спотовый listenKey: {self.spot_listen_key[:15]}...")
                        return self.spot_listen_key
                    else:
                        error_text = await response.text()
                        logging.error(f"❌ Ошибка получения спотового listenKey: {error_text}")
                        return None
        except Exception as e:
            logging.error(f"❌ Исключение при получении спотового listenKey: {e}")
            return None

    async def keepalive_spot_listen_key(self) -> bool:
        """Продление срока действия спотового listenKey"""
        if not self.spot_listen_key:
            return False
            
        endpoint = "/api/v3/userDataStream"
        url = self.spot_base_url + endpoint
        
        headers = {'X-MBX-APIKEY': self.api_key}
        params = {'listenKey': self.spot_listen_key}
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.put(url, headers=headers, params=params, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    if response.status == 200:
                        logging.debug("✅ Спотовый ListenKey успешно продлен")
                        return True
                    else:
                        error_text = await response.text()
                        logging.error(f"❌ Ошибка продления спотового listenKey: {error_text}")
                        return False
        except Exception as e:
            logging.error(f"❌ Исключение при продлении спотового listenKey: {e}")
            return False

    async def connect_spot(self):
        """Подключение к спотовому WebSocket"""
        while self.is_running:
            try:
                # Получаем listenKey
                listen_key = await self.get_spot_listen_key()
                if not listen_key:
                    logging.error("❌ Не удалось получить спотовый listenKey. Повторная попытка через 30 секунд...")
                    await asyncio.sleep(30)
                    continue
                
                # Формируем URL для подключения
                ws_url = f"{self.spot_ws_url}/{listen_key}"
                
                logging.info("🔄 Попытка подключения к спотовому WebSocket...")
                
                async with websockets.connect(
                    ws_url,
                    ping_interval=20,
                    ping_timeout=10,
                    close_timeout=10,
                    max_size=2**23
                ) as websocket:
                    self.spot_websocket = websocket
                    logging.info("✅ Успешное подключение к спотовому WebSocket Binance")
                    print(f"✅ Успешное подключение к спотовому WebSocket - {self.trader_name}")
                    
                    # Запускаем задачи
                    message_task = asyncio.create_task(self.handle_spot_messages())
                    keepalive_task = asyncio.create_task(self.keepalive_spot_loop())
                    reconnect_task = asyncio.create_task(self.schedule_spot_reconnect())
                    
                    done, pending = await asyncio.wait(
                        [message_task, keepalive_task, reconnect_task],
                        return_when=asyncio.FIRST_COMPLETED
                    )
                    
                    for task in pending:
                        task.cancel()
                    
            except Exception as e:
                logging.error(f"❌ Ошибка соединения с спотом: {e}. Переподключение через 10 секунд...")
                await asyncio.sleep(10)

    async def handle_spot_messages(self):
        """Обработка сообщений от спотового WebSocket"""
        try:
            async for message in self.spot_websocket:
                data = json.loads(message)
                await self.process_spot_message(data)
        except Exception as e:
            logging.error(f"❌ Ошибка обработки спотовых сообщений: {e}")
            raise

    async def process_spot_message(self, data: dict):
        """Обработка спотовых сообщений"""
        try:
            event_type = data.get('e', 'UNKNOWN')
            if event_type != 'UNKNOWN':
                logging.debug(f"📨 Спотовое событие {event_type}")
            
            if data.get('e') == 'executionReport' and data['x'] == 'TRADE':
                self.log_spot_trade(data)
                
        except Exception as e:
            logging.error(f"❌ Ошибка обработки спотового сообщения: {e}")

    def log_spot_trade(self, data: dict):
        """Логирование спотовой сделки"""
        try:
            trade_dict = {
            "ordId": data.get('i'),  # orderId из поля 'i'
            "tradeId": data.get('t'),  # tradeId из поля 't'
            "instId": data.get('s', 'UNKNOWN'),  # symbol из поля 's'
            "side": data.get('S', 'UNKNOWN'),  # приводим к нижнему регистру
            "avgPx": data.get('L', '0'),  # цена из поля 'L'
            "state": data.get('X', 'filled'),  # статус из поля 'X'
            "uTime": data.get('T', 0),  # время из поля 'T'
            "fillSz": data.get('l', '0'),  # количество из поля 'l'
            "ordType": data.get('o', 'MARKET')  # тип ордера из поля 'o'
            }
            

            resp = send_trade_to_unity(
                providerAccountId=self.providerAccountId,
                clientAccountId=self.clientAccountId,
                instrumentId=INSTRUMENT_IDS[data['s']],
                side=trade_dict['side'],
                amount=trade_dict['fillSz'],
                price=trade_dict['avgPx'],
                orderId=str(trade_dict['tradeId']),
                comment=self.trader_name)
            
            if resp.status_code == 200:
                logging.info(f'Сделка отправленна в Unity {trade_dict["tradeId"]}')
                is_send = True
            else:
                is_send = False
                logging.error(f"❌ Ошибка при отправке сделки :", resp.status_code, resp.text)

            insert_trade(trade_dict, self.trader_name, is_send)

            
        except Exception as e:
            logging.error(f"❌ Ошибка логирования спотовой сделки: {e}")

    async def keepalive_spot_loop(self):
        """Цикл поддержания активности спотового listenKey"""
        while self.is_running:
            await asyncio.sleep(self.keepalive_interval)
            if self.spot_listen_key:
                success = await self.keepalive_spot_listen_key()
                if not success:
                    logging.error("❌ Не удалось продлить спотовый listenKey. Инициирую переподключение...")
                    break

    async def schedule_spot_reconnect(self):
        """Плановое переподключение для спота"""
        await asyncio.sleep(self.reconnect_interval)
        logging.info("🔄 Инициирование планового переподключения для спота")
        if self.spot_websocket:
            await self.spot_websocket.close()

    async def start_monitoring(self):
        """Запуск мониторинга для фьючерсов и спота"""
        logging.info(f"🚀 Запуск мониторинга для трейдера: {self.trader_name}")
        
        future_task = asyncio.create_task(self.connect_future())
        spot_task = asyncio.create_task(self.connect_spot())
        
        try:
            await asyncio.gather(future_task, spot_task)
        except Exception as e:
            logging.error(f"❌ Критическая ошибка в мониторинге: {e}")
        finally:
            self.is_running = False

    async def stop_monitoring(self):
        """Остановка мониторинга"""
        self.is_running = False
        logging.info("🛑 Остановка мониторинга...")
        
        if self.future_websocket:
            await self.future_websocket.close()
        if self.spot_websocket:
            await self.spot_websocket.close()



async def main_start_ws(API_KEY, SECRET_KEY, TRADER_NAME, providerAccountId, clientAccountId):

    
    monitor = BinanceTradeMonitor(API_KEY, SECRET_KEY, TRADER_NAME,providerAccountId, clientAccountId)
    
    reconnect_attempt = 0
    max_reconnect_attempts = 10
    
    while True:
        try:
            logging.info(f"🔗 Подключаемся к WebSocket (попытка {reconnect_attempt + 1})")
            await monitor.start_monitoring()
            
        except KeyboardInterrupt:
            logging.info("🛑 Получен сигнал прерывания")
            await monitor.stop_monitoring()
            break
            
        except Exception as e:
            reconnect_attempt += 1
            logging.error(f"❌ Ошибка подключения: {e}")
            await monitor.stop_monitoring()
            
            if reconnect_attempt >= max_reconnect_attempts:
                logging.error("🚫 Достигнуто максимальное количество попыток переподключения")
                break
            
            # Экспоненциальная задержка (1, 2, 4, 8, 16... секунд)
            delay = min(2 ** reconnect_attempt, 60)  # Максимум 60 секунд
            logging.info(f"⏳ Повторная попытка через {delay} секунд...")
            await asyncio.sleep(delay)

# # Pavel, [09/09/2025 15:09]
# # # zEiYg23gGA3kPQVOrJO1BQdLUmNrm6OCiZCsBB1pjPuWZlohawm2mE5cZ6iZiBOh

# # # Pavel, [09/09/2025 15:09]
# # # Secret Key
# # # c1oUL5QutbayFBd2knr0pTE9EogjaH2PEeriAtXoRpiGYAM7BynPTDPJju1Gm71j

# if __name__ == "__main__":
#     # Убедитесь, что используете правильную версию websockets
#     # pip install websockets==9.1
#     asyncio.get_event_loop().run_until_complete(main())