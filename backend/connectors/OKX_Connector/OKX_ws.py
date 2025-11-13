import asyncio
import base64
import contextlib
import hmac
import hashlib
import json
import random
import time
from datetime import datetime, timezone
from typing import Iterable, List, Optional
from config import INSTRUMENT_IDS
import aiohttp
from log.logger import get_logger

logger = get_logger(__file__)

from utilites import *




class OkxPrivateFillsMonitor:
    """
    Приватный монитор исполненных сделок (fills) по перпетуалам OKX (*-SWAP).
    - WS login по apiKey/secret/passphrase.
    - Подписка на private 'orders' (instType='SWAP') по заданным instId.
    - Авто-reconnect + плановая ротация каждые 4 часа.
    - Печать служебных сообщений о подключении/подписке.
    - Печать каждого fill: кратко + полный JSON.
    """

    
    SUB_BATCH_SIZE = 20
    PING_INTERVAL_SEC = 20
    MAX_BACKOFF_SEC = 30

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        passphrase: str,
        instruments: Iterable[str],
        providerAccountId: int,
        clientAccountId: int,
        trader_name: str
    ):
        self.api_key = api_key
        self.api_secret = api_secret
        self.passphrase = passphrase
        self.trader_name = trader_name
        self.providerAccountId = providerAccountId
        self.clientAccountId = clientAccountId


        cleaned: List[str] = []
        for i in instruments:
            s = (i or "").strip().upper()
            if s and s.endswith("-SWAP"):
                cleaned.append(s)
        self.instruments = list(dict.fromkeys(cleaned))
        if not self.instruments:
            raise ValueError("Передайте хотя бы один instId вида <BASE>-USD(T)-SWAP, например BTC-USDT-SWAP.")
        

        self.ws_url ="wss://ws.okx.com:8443/ws/v5/private"
        self.reconnect_period_sec = 4 * 60 * 60 # 4 час
        self._running = False

    # --------- утилиты ---------
    @staticmethod
    def _utc_iso(ts_ms: int) -> str:
        return datetime.fromtimestamp(ts_ms / 1000, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3] + "Z"

    @staticmethod
    def _chunk(lst, n):
        for i in range(0, len(lst), n):
            yield lst[i : i + n]

    def _sign(self, ts: str) -> str:
        """ Base64(HMAC_SHA256(secret, ts + 'GET' + '/users/self/verify')) """
        prehash = f"{ts}GET/users/self/verify".encode()
        digest = hmac.new(self.api_secret.encode(), prehash, hashlib.sha256).digest()
        return base64.b64encode(digest).decode()

    @staticmethod
    def _mask(s: str) -> str:
        if not s:
            return "****"
        return f"{s[:4]}***{s[-2:]}"

    # --------- WS действия ---------
    async def _login(self, ws: aiohttp.ClientWebSocketResponse):
        ts = str(time.time())
        sign = self._sign(ts)
        payload = {
            "op": "login",
            "args": [
                {"apiKey": self.api_key, "passphrase": self.passphrase, "timestamp": ts, "sign": sign}
            ],
        }
        await ws.send_json(payload)

        # Ждём ответ об успешном логине
        while True:
            msg = await ws.receive()
            if msg.type != aiohttp.WSMsgType.TEXT:
                raise RuntimeError("Не удалось залогиниться в приватный WS (не TEXT).")
            data = json.loads(msg.data)
            if data.get("event") == "login":
                if data.get("code") == "0":
                    logger.info("Аутентификация OKX WS успешна (apiKey=%s).", self._mask(self.api_key))
                    return
                raise RuntimeError(f"Ошибка логина: {data}")

    async def _send_subscriptions(self, ws: aiohttp.ClientWebSocketResponse):
        # Подписка на private orders по каждому instId (SWAP)
        for batch in self._chunk(self.instruments, self.SUB_BATCH_SIZE):
            args = [{"channel": "orders", "instType": "SWAP", "instId": inst} for inst in batch]
            await ws.send_json({"op": "subscribe", "args": args})
        logger.info("Подписка на 'orders' завершена. Инструменты (%d): %s", len(self.instruments), ", ".join(self.instruments))
        print(f'OKX {self.trader_name} подписка оформлена.')

    async def _heartbeat(self, ws: aiohttp.ClientWebSocketResponse):
        while self._running and not ws.closed:
            try:
                await ws.send_str("ping")  # OKX вернёт "pong"
            except Exception:
                return
            await asyncio.sleep(self.PING_INTERVAL_SEC)

    # --------- обработка данных ---------
    def _print_fill(self, payload: dict):
        """ Печатаем каждое исполнение (fill) кратко + полный JSON сделки. """
        if payload.get("arg", {}).get("channel") != "orders":
            return
    
        for o in payload.get("data", []):
            inst = o.get("instId", "")
            if not inst.endswith("-SWAP") or inst not in self.instruments:
                continue

            fill_px = o.get("fillPx")
            fill_sz = o.get("fillSz")
            try:
                has_fill = (fill_px is not None) and (fill_sz is not None) and float(fill_sz) != 0.0
            except Exception:
                has_fill = False
            if not has_fill:
                continue

            ts_ms = int(o.get("fillTime") or o.get("uTime") or o.get("cTime") or 0)
            iso = self._utc_iso(ts_ms) if ts_ms else "n/a"

            side = o.get("side", "n/a")
            pos_side = o.get("posSide", "n/a")
            ord_id = o.get("ordId", "n/a")
            trade_id = o.get("tradeId") or o.get("fillId") or "n/a"
            exec_type = o.get("execType", "n/a")
            fee = o.get("fee", "n/a")
            fee_ccy = o.get("feeCcy", "n/a")
            # Отправляем в Unity
            rsponse = send_trade_to_unity(
                providerAccountId=self.providerAccountId,
                clientAccountId= self.clientAccountId,
                instrumentId=INSTRUMENT_IDS[inst],
                side=side,
                amount=float(fill_sz),
                price=float(fill_px),
                orderId=ord_id,
                comment=self.trader_name
            )

            logger.info("Получено исполнение: инструмент=%s ordId=%s tradeId=%s сторона=%s px=%s объём=%s", inst, ord_id, trade_id, side, fill_px, fill_sz)

            try:
                status_code = rsponse.status_code if hasattr(rsponse, "status_code") else None
            except Exception:
                status_code = None

            table_name = f"trades_{self.trader_name}"
            if status_code != 200:
                logger.warning("Не удалось отправить сделку в Unity (статус=%s), сохраняю в БД ordId=%s", status_code, ord_id)
                insert_trade(trade=o, db_name=table_name, is_send=False)
            else:
                insert_trade(trade=o, db_name=table_name, is_send=True)


            # Краткая строка
            logger.info("[FILL] [%s] %s ordId=%s tradeId=%s сторона=%s позиция=%s px=%s объём=%s execType=%s комиссия=%s %s",
                        iso, inst, ord_id, trade_id, side, pos_side, fill_px, fill_sz, exec_type, fee, fee_ccy)
            # Полный JSON сделки
            # print("[FILL][JSON] " + json.dumps(o, ensure_ascii=False), flush=True)

    async def _consume(self, ws: aiohttp.ClientWebSocketResponse):
        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                if msg.data == "pong":
                    continue
                try:
                    payload = json.loads(msg.data)
                except json.JSONDecodeError:
                    continue

                # служебные
                if payload.get("event") in {"subscribe", "error"}:
                    # print(payload)  # можно раскомментировать
                    continue

                if payload.get("arg", {}).get("channel") == "orders" and "data" in payload:
                    self._print_fill(payload)

            elif msg.type in (aiohttp.WSMsgType.CLOSED, aiohttp.WSMsgType.ERROR):
                break

    # --------- основной цикл ---------
    async def run(self):
        self._running = True
        backoff = 1.0

        while self._running:
            try:
                timeout = aiohttp.ClientTimeout(total=None, sock_connect=15, sock_read=60)
                async with aiohttp.ClientSession(timeout=timeout) as session:
                    async with session.ws_connect(self.ws_url, heartbeat=None, autoping=False) as ws:
                        logger.info("Соединение установлено: %s", self.ws_url)

                        # login -> subscribe
                        await self._login(ws)
                        await self._send_subscriptions(ws)

                        # параллельные задачи: heartbeat, consumer, таймер ротации
                        hb_task = asyncio.create_task(self._heartbeat(ws))
                        consume_task = asyncio.create_task(self._consume(ws))
                        timer_task = asyncio.create_task(asyncio.sleep(self.reconnect_period_sec))

                        done, _ = await asyncio.wait(
                            {consume_task, timer_task}, return_when=asyncio.FIRST_COMPLETED
                        )

                        # плановая ротация — мягко закрываем сокет
                        if timer_task in done and not ws.closed:
                            logger.info("Плановое переподключение (каждые 4 часа)…")
                            await ws.close(code=1000, message=b"rotate")

                        # уборка задач
                        for t in (hb_task, consume_task, timer_task):
                            if not t.done():
                                t.cancel()
                                with contextlib.suppress(Exception):
                                    await t

                # успешная сессия — сбрасываем бэкофф
                backoff = 1.0
            except Exception as e:
                logger.warning("Соединение оборвалось: %r. Переподключение…", e)
                await asyncio.sleep(backoff + random.uniform(0, 0.5))
                backoff = min(self.MAX_BACKOFF_SEC, backoff * 2)




async def run_okx_monitor(API_KEY, API_SECRET, PASSPHRASE, providerAccountId, clientAccountId, trader_name, instruments):
    """
    Асинхронная функция для запуска монитора OKX
    """
    # Создаем экземпляр монитора
    monitor = OkxPrivateFillsMonitor(
        api_key=API_KEY,
        api_secret=API_SECRET,
        passphrase=PASSPHRASE,
        instruments=instruments,
        providerAccountId=providerAccountId,
        clientAccountId=clientAccountId,
        trader_name=trader_name
    )

    try:
        logger.info("Запуск монитора OKX...")
        await monitor.run()
    except Exception as e:
        logger.error("Ошибка в мониторе OKX: %s", e)
        raise
    finally:
        logger.info("Монитор OKX завершил работу")