from config import *
from hist_trade import HistTrades, get_week_range_ms
from create_bd import TradeDatabase
from Binance_ws import main_start_ws
import traceback
import asyncio
import concurrent.futures
import threading
import time
from datetime import datetime, timedelta
from log.logger import get_logger

logger = get_logger(__file__)

def sync_not_paralel():
    for trader, con in CONFIG_DICT_TEST.items():
        try:
            logger.info(f'Старт обработки трейдера {trader}')
            api_key = con['api_key']
            api_secret = con['api_secret']
            providerAccountId = con['providerAccountId']
            clientAccountId = con['clientAccountId']

            hist = HistTrades(api_key, api_secret)
            db = TradeDatabase(CONFIG_DICT_TEST, trader)

            # stop_symbols = ['1000BONKUSDT', 'DAMUSDT', 'FARTCOINUSDT', 'HYPEUSDT', 'MYXUSDT', 'NAORISUSDT', '1000PEPEUSDT', 'PTBUSDT', 'SAPIENUSDT', '1000SHIBUSDT', 'TAUSDT']

            # for symbol in INSTRUMENT_IDS.keys():

            #     if trader in ['Cap_1', 'Cap_2']:
            #         if symbol not in stop_symbols:
              
            #             buy_margin_trades = hist.margin_hist_trade(symbol)
            #             db.sync_trades_from_list(buy_margin_trades)
                            
            #             sell_margin_trades = hist.get_sell_margin_trades(symbol) # futures !!!
            #             db.sync_trades_from_list(sell_margin_trades)

            #     else:

            #         future_trades = hist.future_hist_trades(symbol)
            #         if symbol not in stop_symbols:
            #             spot_trades = hist.spot_hist_trades(symbol)
                    
            #         db.sync_trades_from_list(spot_trades)
            #         db.sync_trades_from_list(future_trades)

            db.aggregate_and_send_unsent()
           
            logger.info(f'Конец обработки трейдера {trader}')
        except Exception as e:
            logger.error(f'Ошибка: {e}')
            # logger.error(symbol)




if __name__ == '__main__':

    # Основной цикл для синхронной обработки
    try:
        print('Робот Binance запущен!')
        while True:
            try:
                logger.info("Запуск синхронной обработки исторических данных")
                sync_not_paralel()
                logger.info("Синхронная обработка завершена, ожидание 10 мин")
                time.sleep(60 * 5)  
            except Exception as e:
                # Подробное логирование с traceback
                logger.error(f"Ошибка в основном цикле: {e}")
                logger.error(f"Тип ошибки: {type(e).__name__}")
                logger.error(f"Полный traceback:\n{traceback.format_exc()}")
                time.sleep(60 * 10)
                    
    except KeyboardInterrupt:
        print("\nЗавершение по Ctrl+C")
        logger.info("Завершение работы по Ctrl+C")

