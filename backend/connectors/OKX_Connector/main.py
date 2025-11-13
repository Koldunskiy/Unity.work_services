from OKX_ws import run_okx_monitor
from create_bd import TradeDatabase
from historical_trades import OkxFillsFetcher
import asyncio
import threading
import traceback
import time
from concurrent.futures import ThreadPoolExecutor
from config import INSTRUMENT_IDS, CONFIG_DICT_TEST
from log.logger import get_logger

logger = get_logger(__file__)



def sync_not_paralel():
    for trader, con in CONFIG_DICT_TEST.items():
        logger.info(f'Старт обработки трейдера {trader}')
        api_key = con['api_key']
        api_secret = con['api_secret']
        passphrase = con['passphrase']

        hist = OkxFillsFetcher(api_key=api_key, api_secret=api_secret, passphrase=passphrase)
        db = TradeDatabase(CONFIG_DICT_TEST, trader)

        hist_trade = hist.fetch_days()
        db.sync_trades_from_list(hist_trade)

        db.aggregate_and_send_unsent()
        logger.info(f'Конец обработки трейдера {trader}')



def run_async_in_thread(API_KEY, API_SECRET, PASSPHRASE, providerAccountId, clientAccountId, trader_name, instruments):
    """Запускает асинхронную функцию в отдельном потоке"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(run_okx_monitor(API_KEY, API_SECRET, PASSPHRASE, providerAccountId, clientAccountId, trader_name, instruments))
    finally:
        loop.close()
        logger.info(f'Поток для тредера {trader_name} остановлен.')



if __name__ == '__main__':

    try:
        print('Робот OKX запущен!')
        while True:
            try:
                logger.info("Запуск синхронной обработки исторических данных")
                sync_not_paralel()
                logger.info("Синхронная обработка завершена, ожидание 24 часа")
                time.sleep(60 * 3)  
            except Exception as e:
                # Подробное логирование с traceback
                logger.error(f"Ошибка в основном цикле: {e}")
                logger.error(f"Тип ошибки: {type(e).__name__}")
                logger.error(f"Полный traceback:\n{traceback.format_exc()}")
                time.sleep(60 * 4)
                    
    except KeyboardInterrupt:
        print("\nЗавершение по Ctrl+C")
        logger.info("Завершение работы по Ctrl+C")


