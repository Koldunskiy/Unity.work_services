from datetime import datetime, timezone
import requests, json
from log.logger import get_logger
import sqlite3
import traceback
import aiohttp

logger = get_logger(__file__)

def send_trade_to_unity(providerAccountId: int, clientAccountId: int, instrumentId: int, side: str, amount: float, price: float, orderId: str, comment: str = '', timestamp: int = None, commission: float = 0):
    """
    Отправляет сделку в Unity и возвращает объект ответа requests.
    Логирует попытки отправки и ответ сервера.
    """
    # token = "8c132789-d8da-4602-a376-d5e2903e7fba" # test
    token = '9395b23b-82e3-41bc-a8b6-04f9b8a46003' # prod

    # url = "https://rest.portal.stage.unityfinance.net/api/v1/addDirectTrade"  # тестовая среда
    url = "https://rest.unity.finance/api/v1/addDirectTrade"

    if timestamp:
        # Переводим из миллисекунд в секунды
        dt = datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc)

        # Форматы
        transactTime = dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        tradeDate = dt.strftime("%Y-%m-%d")
    else:
        # Получаем текущее время в зоне UTC
        current_time_utc = datetime.now(timezone.utc)

        # Форматируем время в нужные строки
        transactTime = current_time_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
        tradeDate = current_time_utc.strftime("%Y-%m-%d")

    message = {
        "providerAccountId": providerAccountId,
        "clientAccountId": clientAccountId,
        "instrumentId": instrumentId,
        "side": side.upper(),
        "amount": amount,
        "price": price,
        "commission": commission,
        "transactTime": transactTime,
        "tradeDate": tradeDate,
        "valueDate": tradeDate,
        "orderId": orderId,
        "comment": comment,
        "mustBeSendToFix": True, # True !!!!!!!!!
        "skipMarginCheck": False,
        "useExternalCommission": True,
        "clientCloseTradeId": "4"
    }

    headers = {
        "accept": "application/json",
        "auth-token": token,
        "Content-Type": "application/json; charset=utf-8"
    }

    payload = json.dumps(message, indent=4, ensure_ascii=False)
    
    # # Логируем кратко на русском, не выводим в консоль подробный payload
    # logger.info("Отправка сделки в Unity: провайдер=%s клиент=%s инструмент=%s сторона=%s объём=%s цена=%s ордер=%s",
    #             providerAccountId, clientAccountId, instrumentId, side, amount, price, orderId)
    
    try:
        resp = requests.post(url, headers=headers, data=payload.encode('utf-8'), timeout=15)
        # logger.info("Ответ от Unity: статус=%s", resp.status_code)
        return resp
    except Exception as e:
        # logger.exception("Ошибка при отправке сделки в Unity: %s", e)
        raise




def insert_trade(trade: dict, trader_name: str,  is_send = False) -> bool:
    """
    Вставляет одну сделку в таблицу trades.
    Возвращает True, если вставка прошла успешно, False — если ошибка.
    """
    db_path = 'trades.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    db_name = f"trades_{trader_name}"
    try:
        cursor.execute(f'''
            INSERT INTO {db_name} (
                ordId, tradeId, instId, side, avgPx, state, uTime, fillSz, ordType, is_send
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            trade.get("ordId"),
            trade.get("tradeId"),
            trade.get("instId"),
            trade.get("side"),
            float(trade.get("avgPx") or trade.get("fillPx") or 0),
            trade.get("state", "filled"),
            int(trade.get("uTime") or trade.get("ts") or trade.get("fillTime") or 0),
            float(trade.get("fillSz") or trade.get("sz") or 0),
            trade.get("ordType"),
            1 if is_send else 0
        ))
        conn.commit()
        logger.info("insert_trade: inserted ordId=%s tradeId=%s instId=%s", trade.get("ordId"), trade.get("tradeId"), trade.get("instId"))
        return True
    except Exception as e:
        logger.exception("insert_trade failed: %s", e)
        return False
    finally:
        conn.close()
