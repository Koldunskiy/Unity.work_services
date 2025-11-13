# from process_data import send_message
# from auxiliary_files_for_Unity_ideas import Tester_Bot, report_every_day
# import time

# # time.sleep(60 * 60 * 12)
# tester_bot = Tester_Bot()
# # report_every_day()

# if __name__ == "__main__":
#     # Запускаем бота
#     k = 0
#     while True:
#         try:
#             'Шаг 1. Вставляем новые идеи в БД'
#             tester_bot.main_process_data()
#             'Шаг 2. Вставляем новые идеи в БД'
#             strategy_result = tester_bot.take_necessary_data()
#             'Шаг 3. Запись в БД'
#             tester_bot.update_tabel(strategy_result)
#         except Exception as e:
#             print(f'Ошибка в bot_for_Unity_ideas(Ошибкав в теле бота) - {e}')
#         try:
#             'Функция отправки отчетов'
#             if k == 6:
#                 k = 0
#                 report_every_day()
#         except Exception as e:
#             send_message(f'Ошибка в bot_for_Unity_ideas(Ошибкав в отчете) - {e}')
#         k += 1
#         time.sleep(60*60*4)

import threading
import schedule
import time

from process_data import send_message
from auxiliary_files_for_Unity_ideas import Tester_Bot, report_every_day


def start_bot() -> None:
    """Запускает основной цикл бота для обработки данных.

    Создает экземпляр Tester_Bot, обрабатывает данные, получает результаты
    и обновляет таблицу. Повторяет каждые 4 часа.
    """
    tester_bot = Tester_Bot()
    while True:
        try:
            tester_bot.main_process_data()
            strategy_result = tester_bot.take_necessary_data()
            tester_bot.update_tabel(strategy_result)
        except Exception as e:
            send_message(f'Ошибка в bot_for_Unity_ideas (Ошибкав в теле бота) - {e}')
        time.sleep(60 * 60 * 4)  # Пауза на 4 часа


def daily_report() -> None:
    """Запускает ежедневный отчет по расписанию.

    Проверяет расписание и выполняет отчет каждые сутки в 23:00.
    """
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    print('Тестер стратегий заработал.')
    # Настройка расписания для ежедневного отчета
    schedule.every().day.at("23:00").do(report_every_day)

    # Создание потока для ежедневного отчета
    thread_report = threading.Thread(target=daily_report)
    thread_report.start()

    # Создание потока для бота
    thread_bot = threading.Thread(target=start_bot)
    thread_bot.start()