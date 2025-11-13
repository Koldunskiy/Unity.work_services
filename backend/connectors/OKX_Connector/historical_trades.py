import time
import hmac
import json
import base64
import hashlib
import requests
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, List, Optional
from urllib.parse import urljoin, urlencode
from config import INSTRUMENT_IDS
from log.logger import get_logger

logger = get_logger(__file__)

class OkxFillsFetcher:
    """
    Класс для получения исторических сделок (fills) по приватному API OKX (V5)
    + быстрый батч-обогащатель ordType через историю ОРДЕРОВ.

    Идея:
      1) fetch_days(...) — как раньше, тянем fills за окно дат.
      2) build_ordtype_map(...) — один раз тянем историю ОРДЕРОВ за то же окно,
         строим {ordId: ordType}.
      3) enrich_fills_with_ordtype_batch(fills, ...) — одним проходом добавляем ordType в fills.
    """

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        passphrase: str,
        base_url: str = "https://www.okx.com",
        simulated: bool = False,
        timeout: int = 20,
    ):
        self.api_key = api_key
        self.api_secret = api_secret.encode()
        self.passphrase = passphrase
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.simulated = simulated

        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
        logger.debug("Инициализирован OkxFillsFetcher: base_url=%s simulated=%s timeout=%s", self.base_url, self.simulated, self.timeout)

    # ---------- Внутренние утилиты ----------

    @staticmethod
    def _utc_iso_timestamp() -> str:
        # Формат с миллисекундами: 2025-09-04T12:34:56.789Z
        return (
            datetime.now(timezone.utc)
            .isoformat(timespec="milliseconds")
            .replace("+00:00", "Z")
        )

    def _sign(self, ts: str, method: str, request_path: str, body: str = "") -> str:
        """
        Подпись OKX: base64(HMAC_SHA256(secret, ts + method + request_path + body))
        request_path должен включать query-параметры (если есть).
        """
        presign = f"{ts}{method.upper()}{request_path}{body}"
        digest = hmac.new(self.api_secret, presign.encode(), hashlib.sha256).digest()
        return base64.b64encode(digest).decode()

    def _auth_headers(self, ts: str, sign: str) -> Dict[str, str]:
        headers = {
            "OK-ACCESS-KEY": self.api_key,
            "OK-ACCESS-SIGN": sign,
            "OK-ACCESS-TIMESTAMP": ts,
            "OK-ACCESS-PASSPHRASE": self.passphrase,
        }
        if self.simulated:
            headers["x-simulated-trading"] = "1"
        return headers

    def _request(self, path: str, params: Dict[str, str]) -> Dict[str, Any]:
        """
        Делает подписанный GET-запрос. params одновременно идут в запрос и используются в подписи.
        Важно: request_path в подписи включает ?query в том же порядке.
        """
        url = urljoin(self.base_url, path)
        query = urlencode(list(params.items())) if params else ""
        request_path = f"{path}?{query}" if query else path

        ts = self._utc_iso_timestamp()
        sign = self._sign(ts, "GET", request_path, "")
        headers = self._auth_headers(ts, sign)

        logger.debug("Запрос к OKX: %s", request_path)
        resp = self.session.get(url, headers=headers, params=params, timeout=self.timeout)
        resp.raise_for_status()
        data = resp.json()
        code = data.get("code")
        if str(code) not in ("0", "00000"):
            raise RuntimeError(f"OKX API error: code={code}, msg={data.get('msg')}, data={data}")
        return data

    @staticmethod
    def _extract_min_ts_ms(items: List[Dict[str, Any]]) -> Optional[int]:
        """
        Находит минимальную метку времени (в мс) в странице результатов.
        Для fills: 'fillTime' (или 'ts'/'uTime'). Для orders — обычно 'uTime' или 'cTime'.
        """
        min_ts = None
        for it in items:
            ts_str = it.get("fillTime") or it.get("ts") or it.get("uTime") or it.get("cTime")
            if ts_str is None:
                continue
            try:
                ts = int(ts_str)
                if min_ts is None or ts < min_ts:
                    min_ts = ts
            except Exception:
                continue
        return min_ts

    @staticmethod
    def _window_ms(days: int):
        if days is None or days <= 0:
            days = 7
        now = datetime.now(timezone.utc)
        begin = now - timedelta(days=days)
        return int(begin.timestamp() * 1000), int(now.timestamp() * 1000)

    # ---------- Fills ----------

    def fetch_days(
        self,
        days: int = 7,
        *,
        instType: str = "SWAP",
        instId: Optional[str] = None,
        uly: Optional[str] = None,
        limit: int = 100,
        max_pages: int = 1000,
        sleep_sec: float = 0.1,
    ) -> List[Dict[str, Any]]:
        """
        Забирает исторические сделки (fills) за указанное число дней.
        """
        begin_ms, end_ms = self._window_ms(days)
        logger.debug("fetch_days: дни=%s тип=%s instId=%s окно_begin=%s окно_end=%s", days, instType, instId, begin_ms, end_ms)
        results: List[Dict[str, Any]] = []
        pages = 0

        path = "/api/v5/trade/fills-history"

        while pages < max_pages:
            params: Dict[str, str] = {
                "instType": instType,
                "limit": str(limit),
                "begin": str(begin_ms),
                "end": str(end_ms),
            }
            if instId:
                params["instId"] = instId
            if uly:
                params["uly"] = uly

            payload = self._request(path, params)
            items: List[Dict[str, Any]] = payload.get("data", []) or []
            if not items:
                break

            results.extend(items)
            pages += 1

            # Сдвигаем окно назад, чтобы не ловить дубли
            min_ts = self._extract_min_ts_ms(items)
            if min_ts is None:
                break
            new_end = min_ts - 1
            if new_end <= begin_ms:
                break
            end_ms = new_end

            if len(items) < limit:
                break

            if sleep_sec > 0:
                time.sleep(sleep_sec)

        return self.enrich_fills_with_ordtype_batch(results, days=days, instType=instType) 

    # ---------- История ордеров -> карта ordId -> ordType ----------

    def _fetch_orders_page(
        self,
        path: str,
        params: Dict[str, str],
    ) -> List[Dict[str, Any]]:
        """
        Универсальная выборка страницы для history / history-archive.
        Возвращает список объектов из 'data'.
        """
        payload = self._request(path, params)
        return payload.get("data", []) or []

    def build_ordtype_map(
        self,
        days: int = 7,
        *,
        instType: str = "SWAP",
        instId: Optional[str] = None,
        uly: Optional[str] = None,
        limit: int = 100,
        max_pages: int = 200,
        sleep_sec: float = 0.1,
        use_archive_if_needed: bool = True,
    ) -> Dict[str, str]:
        """
        Собирает карту {ordId: ordType} за окно дат.
        Сначала идёт по /orders-history (последние ~7 дней),
        при необходимости — по /orders-history-archive (до 3 месяцев).
        Пагинация реализована курсором 'before' по последнему ordId (распространённый паттерн OKX).
        Мы фильтруем записи по времени (uTime/cTime) сами, чтобы не уходить глубже окна.
        """
        begin_ms, end_ms = self._window_ms(days)
        logger.debug("build_ordtype_map: дни=%s тип=%s instId=%s", days, instType, instId)
        ord_map: Dict[str, str] = {}

        def collect_from_endpoint(path: str) -> bool:
            pages = 0
            before = None
            while pages < max_pages:
                params: Dict[str, str] = {
                    "instType": instType,
                    "limit": str(limit),
                }
                if instId:
                    params["instId"] = instId
                if uly:
                    params["uly"] = uly
                if before:
                    params["before"] = before  # курсор пагинации — id (обычно ordId / billId)

                items = self._fetch_orders_page(path, params)
                if not items:
                    return True  # закончились

                pages += 1

                # Отберём только записи внутри окна по uTime/cTime
                for it in items:
                    ts_str = it.get("uTime") or it.get("cTime") or it.get("ts")
                    try:
                        ts = int(ts_str) if ts_str is not None else None
                    except Exception:
                        ts = None

                    if ts is not None and ts < begin_ms:
                        # Мы дошли ниже нижней границы окна — можно останавливать сбор
                        return True

                    ord_id = it.get("ordId")
                    ord_type = it.get("ordType")
                    if ord_id and ord_type and (ts is None or ts <= end_ms):
                        ord_map.setdefault(ord_id, ord_type)

                # курсор на следующую страницу:
                last = items[-1]
                before = last.get("ordId") or last.get("billId") or last.get("id")
                if not before:
                    # Если нет явного курсора — попробуем сместиться по времени:
                    min_ts = self._extract_min_ts_ms(items)
                    if not min_ts or min_ts <= begin_ms:
                        return True

                if len(items) < limit:
                    return True  # последняя страница

                if sleep_sec > 0:
                    time.sleep(sleep_sec)

            return False  # вышли по max_pages

        # 1) Основная история (обычно покрывает последние 7 дней)
        done = collect_from_endpoint("/api/v5/trade/orders-history")
        if not done:
            # достигли max_pages
            pass

        # 2) Если не хватило, можно дособрать из архива
        if use_archive_if_needed:
            # Если окно > 7 дней, или карта всё ещё пустая/неполная — качаем архив
            collect_from_endpoint("/api/v5/trade/orders-history-archive")

        return ord_map

    def enrich_fills_with_ordtype_batch(
        self,
        fills: List[Dict[str, Any]],
        days: int = 7,
        *,
        instType: str = "SWAP",
        instId: Optional[str] = None,
        uly: Optional[str] = None,
        limit: int = 100,
        max_pages: int = 200,
        sleep_sec: float = 0.1,
        use_archive_if_needed: bool = True,
    ) -> List[Dict[str, Any]]:
        """
        Обогащает список fills полем 'ordType' с помощью карты из истории ордеров.
        Ничего лишнего не запрашивает после построения карты.
        """
        ordtype_map = self.build_ordtype_map(
            days=days,
            instType=instType,
            instId=instId,
            uly=uly,
            limit=limit,
            max_pages=max_pages,
            sleep_sec=sleep_sec,
            use_archive_if_needed=use_archive_if_needed,
        )
        logger.debug("Обогащение fills: найдено типов_ord=%d, fills=%d", len(ordtype_map), len(fills))
        out = []
        for f in fills:
            oid = f.get("ordId")
            if oid and oid in ordtype_map:
                f["ordType"] = ordtype_map[oid]
                out.append(f)
            else:
                out.append(f)  # без изменений, если не нашли
        return out


