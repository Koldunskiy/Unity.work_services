from process_data import main_data_processing, vizual, send_message
from datetime import datetime
import requests
import telebot
import os
from settings import TOKEN, TG_CH
import logging

# Конфигурирование логгера
logging.basicConfig(filename='app.log', level=logging.INFO)

'''Рабочие значения токена'''
TOKEN = TOKEN
TG_CH = TG_CH
URL = 'https://api.telegram.org/bot'

bot = telebot.TeleBot(TOKEN)


def send_document_file(path_to_file: str) -> None:
    """Отправляет документ в Telegram-чат.

    Args:
        path_to_file (str): Путь к файлу для отправки.
    """
    files = {'document': open(path_to_file, 'rb')}
    requests.post(f'{URL}{TOKEN}/sendDocument?chat_id={TG_CH}', files=files)


@bot.message_handler(content_types=['document'])
def handle_document(message) -> None:
    """Обработчик входящих документов в Telegram-боте.

    Проверяет, является ли файл .xlsx, скачивает его, обрабатывает данные,
    визуализирует и отправляет обратно. Удаляет файл после обработки.

    Args:
        message: Сообщение от Telegram с документом.
    """
    global FILE_NAME
    # Проверяем, является ли прикрепленный файл .xlsx
    if message.document.file_name.endswith('.xlsx'):
        # Скачиваем файл
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        # Сохраняем файл
        FILE_NAME = f'Отчет_по_стратегиям_за_{datetime.now().strftime("%d.%m.%Y")}.xlsx'
        with open(FILE_NAME, 'wb') as new_file:
            new_file.write(downloaded_file)

        # Отвечаем пользователю
        bot.reply_to(message, "Отчет приянт.")
        main_data_processing(FILE_NAME)
        vizual(FILE_NAME)
        send_document_file(FILE_NAME)
        os.remove(FILE_NAME)


if __name__ == "__main__":
    # Запускаем бота
    try:
        print('swap_bot')
        bot.polling(none_stop=True)
    except Exception as e:
        # Логирование ошибки
        logging.error(f"Ошибка в тестере стратегий: {str(e)}", exc_info=True)
        send_message(f"Ошибка в тестере стратегий: {str(e)}", mod=0)