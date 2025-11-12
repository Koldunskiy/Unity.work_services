import threading
import logging
import time
import re
import pandas as pd
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from pybit.unified_trading import HTTP
from dop import send_unsended_orders, main

# --- Настройка логирования ---
LOG_FILE = "bot.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

# --- Функция PАМ, выполняемая в отдельном потоке ---
def pam_main():
    """Функция выполняется в фоновом потоке, каждые 15 минут запускает main()."""
    while True:
        try:
            logging.info("Запуск pam_main()...")
            main()
            logging.info("pam_main() выполнен успешно.")
        except Exception as e:
            logging.error(f"Ошибка в pam_main(): {e}")
        time.sleep(15 * 60)  # Ждем 15 минут перед следующим запуском

# --- Настройка Telegram-бота ---
bot_token = '7699618218:AAHEjT-wxs1aV8beVLDKiiOWq1--ZMEXqNM'
bot = telebot.TeleBot(bot_token)

# Регулярное выражение для проверки формата "строка - id(int)"
pattern = re.compile(r'^\s*([\w\s]+)\s*-\s*(\d+)\s*$')

# --- Функция клавиатуры ---
def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("Добавить данные"), KeyboardButton("Загрузить данные"))
    return markup

# --- Обработчики бота ---
@bot.message_handler(commands=['start'])
def start_message(message):
    logging.info(f"Команда /start от пользователя {message.chat.id}")
    bot.send_message(
        message.chat.id, 
        "Привет! Выберите действие:", 
        reply_markup=main_menu()
    )

@bot.message_handler(func=lambda message: message.text == "Добавить данные")
def request_data(message):
    logging.info(f"Пользователь {message.chat.id} выбрал 'Добавить данные'")
    bot.send_message(message.chat.id, "Введите данные в формате: SYMBOL - id.")

@bot.message_handler(func=lambda message: message.text == "Загрузить данные")
def load_data(message):
    logging.info(f"Пользователь {message.chat.id} выбрал 'Загрузить данные'")
    bot.send_message(message.chat.id, "Функция загрузки пока не реализована.")
    send_unsended_orders()

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text.strip()
    match = pattern.match(text)

    if match:
        symbol = match.group(1).strip()
        user_id = int(match.group(2))
        file_path = 'U_SYMBOLS_ID.csv'

        try:
            df = pd.read_csv(file_path)
        except FileNotFoundError:
            df = pd.DataFrame(columns=['symbol', 'id'])

        if symbol not in df['symbol'].values:
            new_data = pd.DataFrame([[symbol, user_id]], columns=['symbol', 'id'])
            new_data.to_csv(file_path, mode='a', header=False, index=False)

            logging.info(f"Добавлены данные: {symbol} - {user_id}")
            bot.send_message(message.chat.id, f"✅ Данные добавлены: {symbol} - {user_id}")
        else:
            logging.warning(f"Попытка добавить дубликат: {symbol}, ID: {user_id}")
            bot.send_message(message.chat.id, f"⚠ Такой символ уже есть: {symbol}, ID: {user_id}")
    else:
        logging.warning(f"Некорректный ввод от пользователя {message.chat.id}: {text}")
        bot.send_message(message.chat.id, "❌ Неверный формат! Введите данные в формате 'строка - id'.")

# --- Запуск потока PАМ ---
logging.info("Запуск фонового потока для pam_main()...")
pam_thread = threading.Thread(target=pam_main, daemon=True)
pam_thread.start()

# --- Запуск бота ---
logging.info("Бот ПАМ запущен. Ожидание сообщений...")
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logging.error(f"Ошибка в Telegram-боте: {e}")
        time.sleep(5)  # Ожидание перед повторным запуском
