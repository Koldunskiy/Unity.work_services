"""
Модуль для мониторинга сделок на Binance (спот и фьючерсы) через WebSocket.
Обрабатывает события исполнения ордеров и отправляет их в Unity Finance.
"""

import asyncio
import json
import hmac
import hashlib
import logging
import urllib.parse
from datetime import datetime
from typing import Optional, Dict, Any

import aiohttp
import websockets
from log.logger import get_logger
from utilites import send_trade_to_unity, insert_trade
from config import INSTRUMENT_IDS


# Настройка логгера
logging = get_logger(__file__)


class BinanceTradeMonitor:
    """
    Мониторит сделки на Binance (спот и фьючерсы) через WebSocket.
    Отправляет исполненные ордера в Unity Finance и сохраняет в БД.
    """

    def __init__(
        self,
        api_key: str,
        secret_key: str,
        trader_name: str,
        provider_account_id: int,
        client_account_id: int
    ) -> None:
        """
        Инициализация мониторинга для конкретного трейдера.

        Args:
            api_key (str): API-ключ Binance.
            secret_key (str): Секретный ключ Binance.
            trader_name (str): Имя трейдера (для логирования и комментариев).
            provider_account_id (int): ID провайдера в Unity.
            client_account_id (int): ID клиента в Unity.
        """
        self.api_key = api_key
        self.secret_key = secret_key
        self.trader_name = trader_name
        self.provider_account_id = provider_account_id
        self.client_account_id = client_account_id

        # Фьючерсы
        self.future_base_url = "https://fapi.binance.com"
        self.future_ws_url = "wss://fstream.binance.com/ws"
        self.future_listen_key: Optional[str] = None
        self.future_websocket: Optional[websockets.WebSocketClientProtocol] = None

        # Спот
        self.spot_base_url = "https://api.binance.com"
        self.spot_ws_url = "wss://stream.binance.com:9443/ws"
        self.spot_listen_key: Optional[str] = None
        self.spot_websocket: Optional[websockets.WebSocketClientProtocol] = None

        # Общие настройки
        self.reconnect_interval = 10 * 3600  # 10 часов (меньше 12)
        self.keepalive_interval = 25 * 60    # 25 минут (меньше 30)
        self.is_running = True

    # ============================================================================
    # Вспомогательные методы
    # ============================================================================

    def generate_signature(self, params: Dict[str, Any]) -> str:
        """
        Генерирует HMAC-SHA256 подпись для параметров запроса.

        Args:
            params (Dict[str, Any]): Параметры запроса.

        Returns:
            str: Подпись в виде hex-строки.
        """
        query_string = urllib.parse.urlencode(params)
        return hmac.new(
            self.secret_key.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

    # ============================================================================
    # ФЬЮЧЕРСЫ: listenKey и подключение
    # ============================================================================

    async def get_future_listen_key(self) -> Optional[str]:
        """
        Получает listenKey для фьючерсного WebSocket.

        Returns:
            Optional[str]: listenKey или None при ошибке.
        """
        endpoint = "/fapi/v1/listenKey"
        url = self.future_base_url + endpoint
        headers = {'X-MBX-APIKEY': self.api_key}

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    if response.status == 200:
                        data = await response.json()
                        self.future_listen_key = data['listenKey']
                        logging.info(f"Получен фьючерсный listenKey: {self.future_listen_key[:15]}...")
                        return self.future_listen_key
                    else:
                        error_text = await response.text()
                        logging.error(f"Ошибка получения фьючерсного listenKey: {error_text}")
                        return None
        except Exception as e:
            logging.error(f"Исключение при получении фьючерсного listenKey: {e}")
            return None

    async def keepalive_future_listen_key(self) -> bool:
        """
        Продлевает срок действия фьючерсного listenKey.

        Returns:
            bool: True при успехе.
        """
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
                        logging.debug("Фьючерсный ListenKey успешно продлён")
                        return True
                    else:
                        error_text = await response.text()
                        logging.error(f"Ошибка продления фьючерсного listenKey: {error_text}")
                        return False
        except Exception as e:
            logging.error(f"Исключение при продлении фьючерсного listenKey: {e}")
            return False

    async def connect_future(self) -> None:
        """
        Устанавливает и поддерживает соединение с фьючерсным WebSocket.
        """
        while self.is_running:
            try:
                listen_key = await self.get_future_listen_key()
                if not listen_key:
                    logging.error("Не удалось получить фьючерсный listenKey. Повтор через 30 сек...")
                    await asyncio.sleep(30)
                    continue

                ws_url = f"{self.future_ws_url}/{listen_key}"
                logging.info("Попытка подключения к фьючерсному WebSocket...")

                async with websockets.connect(
                    ws_url,
                    ping_interval=20,
                    ping_timeout=10,
                    close_timeout=10,
                    max_size=2**23  # 8MB
                ) as websocket:
                    self.future_websocket = websocket
                    logging.info("Успешное подключение к фьючерсному WebSocket Binance")
                    print(f"Успешное подключение к фьючерсному WebSocket - {self.trader_name}")

                    # Запуск задач
                    message_task = asyncio.create_task(self.handle_future_messages())
                    keepalive_task = asyncio.create_task(self.keepalive_future_loop())
                    reconnect_task = asyncio.create_task(self.schedule_future_reconnect())

                    done, pending = await asyncio.wait(
                        [message_task, keepalive_task, reconnect_task],
                        return_when=asyncio.FIRST_COMPLETED
                    )

                    for task in pending:
                        task.cancel()

            except websockets.exceptions.ConnectionClosed as e:
                logging.error(f"Фьючерсное соединение закрыто: {e}. Переподключение через 10 сек...")
                await asyncio.sleep(10)
            except Exception as e:
                logging.error(f"Ошибка соединения с фьючерсами: {e}. Переподключение через 10 сек...")
                await asyncio.sleep(10)

    async def handle_future_messages(self) -> None:
        """
        Обрабатывает входящие сообщения от фьючерсного WebSocket.
        """
        try:
            async for message in self.future_websocket:
                try:
                    data = json.loads(message)
                    await self.process_future_message(data)
                except json.JSONDecodeError as e:
                    logging.error(f"Ошибка декодирования JSON: {e}, сообщение: {message[:100]}")
                except Exception as e:
                    logging.error(f"Ошибка обработки сообщения: {e}")
        except websockets.exceptions.ConnectionClosed:
            logging.warning("Фьючерсное соединение закрыто")
        except Exception as e:
            logging.error(f"Ошибка в handle_future_messages: {e}")
            raise

    async def process_future_message(self, data: dict) -> None:
        """
        Обрабатывает конкретное сообщение от фьючерсов.

        Args:
            data (dict): JSON-сообщение.
        """
        try:
            event_type = data.get('e', 'UNKNOWN')
            logging.debug(f"Фьючерсное событие: {event_type}")

            if event_type == 'ORDER_TRADE_UPDATE':
                order_data = data['o']
                if order_data.get('x') == 'TRADE':
                    self.log_future_trade(order_data, data['E'])

            elif event_type == 'ACCOUNT_UPDATE':
                logging.info("Обновление фьючерсного аккаунта")

            elif event_type == 'listenKeyExpired':
                logging.warning("Фьючерсный listenKey истёк, требуется переподключение")
                if self.future_websocket:
                    await self.future_websocket.close()

        except Exception as e:
            logging.error(f"Ошибка обработки фьючерсного сообщения: {e}")

    def log_future_trade(self, order_data: dict, event_time: int) -> None:
        """
        Логирует и отправляет фьючерсную сделку в Unity.

        Args:
            order_data (dict): Данные ордера.
            event_time (int): Время события.
        """
        try:
            trade_dict = {
                "ordId": order_data.get('i'),
                "tradeId": order_data.get('t'),
                "instId": order_data.get('s', 'UNKNOWN'),
                "side": order_data.get('S', 'UNKNOWN'),
                "avgPx": order_data.get('L', '0'),
                "state": order_data.get('X', 'filled'),
                "uTime": order_data.get('T', 0),
                "fillSz": order_data.get('l', '0'),
                "ordType": order_data.get('o', 'MARKET')
            }

            resp = send_trade_to_unity(
                providerAccountId=self.provider_account_id,
                clientAccountId=self.client_account_id,
                instrumentId=INSTRUMENT_IDS.get(order_data['s']),
                side=trade_dict['side'],
                amount=trade_dict['fillSz'],
                price=trade_dict['avgPx'],
                orderId=str(trade_dict['tradeId']),
                comment=self.trader_name
            )

            is_send = resp.status_code == 200
            if is_send:
                logging.info(f'Сделка отправлена в Unity: {trade_dict["tradeId"]}')
            else:
                logging.error(f"Ошибка при отправке сделки: {resp.status_code} {resp.text}")

            insert_trade(trade_dict, self.trader_name, is_send)

        except Exception as e:
            logging.error(f"Ошибка логирования фьючерсной сделки: {e}")

    async def keepalive_future_loop(self) -> None:
        """Цикл продления фьючерсного listenKey."""
        while self.is_running:
            await asyncio.sleep(self.keepalive_interval)
            if self.future_listen_key:
                success = await self.keepalive_future_listen_key()
                if not success:
                    logging.error("Не удалось продлить фьючерсный listenKey. Переподключение...")
                    break

    async def schedule_future_reconnect(self) -> None:
        """Плановое переподключение фьючерсов."""
        await asyncio.sleep(self.reconnect_interval)
        logging.info("Инициирование планового переподключения фьючерсов")
        if self.future_websocket:
            await self.future_websocket.close()

    # ============================================================================
    # СПOT: listenKey и подключение
    # ============================================================================

    async def get_spot_listen_key(self) -> Optional[str]:
        """
        Получает listenKey для спотового WebSocket.

        Returns:
            Optional[str]: listenKey или None.
        """
        endpoint = "/api/v3/userDataStream"
        url = self.spot_base_url + endpoint
        headers = {'X-MBX-APIKEY': self.api_key}

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    if response.status == 200:
                        data = await response.json()
                        self.spot_listen_key = data['listenKey']
                        logging.info(f"Получен спотовый listenKey: {self.spot_listen_key[:15]}...")
                        return self.spot_listen_key
                    else:
                        error_text = await response.text()
                        logging.error(f"Ошибка получения спотового listenKey: {error_text}")
                        return None
        except Exception as e:
            logging.error(f"Исключение при получении спотового listenKey: {e}")
            return None

    async def keepalive_spot_listen_key(self) -> bool:
        """
        Продлевает спотовый listenKey.

        Returns:
            bool: True при успехе.
        """
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
                        logging.debug("Спотовый ListenKey успешно продлён")
                        return True
                    else:
                        error_text = await response.text()
                        logging.error(f"Ошибка продления спотового listenKey: {error_text}")
                        return False
        except Exception as e:
            logging.error(f"Исключение при продлении спотового listenKey: {e}")
            return False

    async def connect_spot(self) -> None:
        """
        Устанавливает и поддерживает соединение со спотовым WebSocket.
        """
        while self.is_running:
            try:
                listen_key = await self.get_spot_listen_key()
                if not listen_key:
                    logging.error("Не удалось получить спотовый listenKey. Повтор через 30 сек...")
                    await asyncio.sleep(30)
                    continue

                ws_url = f"{self.spot_ws_url}/{listen_key}"
                logging.info("Попытка подключения к спотовому WebSocket...")

                async with websockets.connect(
                    ws_url,
                    ping_interval=20,
                    ping_timeout=10,
                    close_timeout=10,
                    max_size=2**23
                ) as websocket:
                    self.spot_websocket = websocket
                    logging.info("Успешное подключение к спотовому WebSocket Binance")
                    print(f"Успешное подключение к спотовому WebSocket - {self.trader_name}")

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
                logging.error(f"Ошибка соединения со спотом: {e}. Переподключение через 10 сек...")
                await asyncio.sleep(10)

    async def handle_spot_messages(self) -> None:
        """
        Обрабатывает входящие сообщения от спотового WebSocket.
        """
        try:
            async for message in self.spot_websocket:
                try:
                    data = json.loads(message)
                    await self.process_spot_message(data)
                except json.JSONDecodeError as e:
                    logging.error(f"Ошибка декодирования JSON: {e}")
                except Exception as e:
                    logging.error(f"Ошибка обработки спотового сообщения: {e}")
        except Exception as e:
            logging.error(f"Ошибка в handle_spot_messages: {e}")
            raise

    async def process_spot_message(self, data: dict) -> None:
        """
        Обрабатывает конкретное спотовое сообщение.

        Args:
            data (dict): JSON-сообщение.
        """
        try:
            event_type = data.get('e', 'UNKNOWN')
            logging.debug(f"Спотовое событие: {event_type}")

            if data.get('e') == 'executionReport' and data.get('x') == 'TRADE':
                self.log_spot_trade(data)

        except Exception as e:
            logging.error(f"Ошибка обработки спотового сообщения: {e}")

    def log_spot_trade(self, data: dict) -> None:
        """
        Логирует и отправляет спотовую сделку в Unity.

        Args:
            data (dict): Данные исполнения.
        """
        try:
            trade_dict = {
                "ordId": data.get('i'),
                "tradeId": data.get('t'),
                "instId": data.get('s', 'UNKNOWN'),
                "side": data.get('S', 'UNKNOWN'),
                "avgPx": data.get('L', '0'),
                "state": data.get('X', 'filled'),
                "uTime": data.get('T', 0),
                "fillSz": data.get('l', '0'),
                "ordType": data.get('o', 'MARKET')
            }

            resp = send_trade_to_unity(
                providerAccountId=self.provider_account_id,
                clientAccountId=self.client_account_id,
                instrumentId=INSTRUMENT_IDS.get(data['s']),
                side=trade_dict['side'],
                amount=trade_dict['fillSz'],
                price=trade_dict['avgPx'],
                orderId=str(trade_dict['tradeId']),
                comment=self.trader_name
            )

            is_send = resp.status_code == 200
            if is_send:
                logging.info(f'Сделка отправлена в Unity: {trade_dict["tradeId"]}')
            else:
                logging.error(f"Ошибка при отправке сделки: {resp.status_code} {resp.text}")

            insert_trade(trade_dict, self.trader_name, is_send)

        except Exception as e:
            logging.error(f"Ошибка логирования спотовой сделки: {e}")

    async def keepalive_spot_loop(self) -> None:
        """Цикл продления спотового listenKey."""
        while self.is_running:
            await asyncio.sleep(self.keepalive_interval)
            if self.spot_listen_key:
                success = await self.keepalive_spot_listen_key()
                if not success:
                    logging.error("Не удалось продлить спотовый listenKey. Переподключение...")
                    break

    async def schedule_spot_reconnect(self) -> None:
        """Плановое переподключение спота."""
        await asyncio.sleep(self.reconnect_interval)
        logging.info("Инициирование планового переподключения спота")
        if self.spot_websocket:
            await self.spot_websocket.close()

    # ============================================================================
    # Управление мониторингом
    # ============================================================================

    async def start_monitoring(self) -> None:
        """
        Запускает мониторинг фьючерсов и спота одновременно.
        """
        logging.info(f"Запуск мониторинга для трейдера: {self.trader_name}")

        future_task = asyncio.create_task(self.connect_future())
        spot_task = asyncio.create_task(self.connect_spot())

        try:
            await asyncio.gather(future_task, spot_task)
        except Exception as e:
            logging.error(f"Критическая ошибка в мониторинге: {e}")
        finally:
            self.is_running = False

    async def stop_monitoring(self) -> None:
        """
        Останавливает мониторинг и закрывает соединения.
        """
        self.is_running = False
        logging.info("Остановка мониторинга...")

        if self.future_websocket:
            await self.future_websocket.close()
        if self.spot_websocket:
            await self.spot_websocket.close()


# ============================================================================
# Точка входа
# ============================================================================

async def main_start_ws(
    api_key: str,
    secret_key: str,
    trader_name: str,
    provider_account_id: int,
    client_account_id: int
) -> None:
    """
    Запускает WebSocket-мониторинг с автоматическим переподключением.

    Args:
        api_key (str): API-ключ.
        secret_key (str): Секретный ключ.
        trader_name (str): Имя трейдера.
        provider_account_id (int): ID провайдера.
        client_account_id (int): ID клиента.
    """
    monitor = BinanceTradeMonitor(api_key, secret_key, trader_name, provider_account_id, client_account_id)

    reconnect_attempt = 0
    max_reconnect_attempts = 10

    while True:
        try:
            logging.info(f"Подключаемся к WebSocket (попытка {reconnect_attempt + 1})")
            await monitor.start_monitoring()

        except KeyboardInterrupt:
            logging.info("Получен сигнал прерывания")
            await monitor.stop_monitoring()
            break

        except Exception as e:
            reconnect_attempt += 1
            logging.error(f"Ошибка подключения: {e}")
            await monitor.stop_monitoring()

            if reconnect_attempt >= max_reconnect_attempts:
                logging.error("Достигнуто максимальное количество попыток переподключения")
                break

            delay = min(2 ** reconnect_attempt, 60)
            logging.info(f"Повторная попытка через {delay} секунд...")
            await asyncio.sleep(delay)


# Пример запуска (раскомментировать при необходимости)
# if __name__ == "__main__":
#     asyncio.run(main_start_ws(
#         api_key="zEiYg23gGA3kPQVOrJO1BQdLUmNrm6OCiZCsBB1pjPuWZlohawm2mE5cZ6iZiBOh",
#         secret_key="c1oUL5QutbayFBd2knr0pTE9EogjaH2PEeriAtXoRpiGYAM7BynPTDPJju1Gm71j",
#         trader_name="Pavel",
#         provider_account_id=1,
#         client_account_id=2
#     ))