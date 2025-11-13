

# import pandas as pd
# import datetime
# from dop_files import result_string

# import telebot
# from telebot import types

# KEY_BOT_MANGER_MT5 = '7840597904:AAHrwP2adJsCLSg3myhTDEW-eJ4gtujG-UU'
# bot = telebot.TeleBot(KEY_BOT_MANGER_MT5)

# # Глобальная переменная для хранения выбранного провайдера
# selected_provider = None
# # bot.send_message(620211681, "Думаю...")

# # Обработчик команды /start
# @bot.message_handler(commands=['start'])
# def send_provider_choice(message):
#     # Создание клавиатуры для выбора провайдера
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     provider1_button = types.KeyboardButton("Neo MU")
#     provider2_button = types.KeyboardButton("Active Broker")
#     markup.add(provider1_button, provider2_button)
    
#     # Отправка сообщения с выбором провайдера
#     bot.send_message(message.chat.id, "Выберите провайдера:", reply_markup=markup)

# # Функция для создания основного меню после выбора провайдера
# def send_main_menu(chat_id):

#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     button1 = types.KeyboardButton("Баланс")
#     button2 = types.KeyboardButton("PNL")
#     button3 = types.KeyboardButton("Equity")
#     button4 = types.KeyboardButton("Назад")
#     markup.add(button1, button2, button3, button4)
    
#     bot.send_message(chat_id, "Выберите опцию:", reply_markup=markup)

# # Функция для создания подменю с кнопками дат
# def send_submenu(chat_id, main_option):
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     sub_button1 = types.KeyboardButton(f"{main_option} - Сегодня")
#     sub_button2 = types.KeyboardButton(f"{main_option} - Вчера")
#     sub_button3 = types.KeyboardButton(f"{main_option} - Текущая неделя")
#     sub_button4 = types.KeyboardButton(f"{main_option} - Текущий месяц")
#     back_button = types.KeyboardButton("Назад")
#     markup.add(sub_button1, sub_button2, sub_button3, sub_button4, back_button)
#     bot.send_message(chat_id, f"Вы выбрали {main_option}. Выберите период:", reply_markup=markup)

# # Функции для получения нужной даты
# def get_today():
#     return datetime.date.today().strftime('%Y-%m-%d'), datetime.date.today().strftime('%Y-%m-%d')

# def get_yesterday():
#     return (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d'), (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')

# def get_week():
#     start_of_week = datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday())
#     return start_of_week.strftime('%Y-%m-%d'), datetime.date.today().strftime('%Y-%m-%d')

# def get_month():
#     start_of_month = datetime.date.today().replace(day=1)
#     return start_of_month.strftime('%Y-%m-%d'), datetime.date.today().strftime('%Y-%m-%d')

# # Обработчик текстовых сообщений
# @bot.message_handler(func=lambda message: True)
# def handle_message(message):
#     global selected_provider

#     # Проверка выбора провайдера
#     if message.text == "Neo MU":
#         selected_provider = "NEO"
#         send_main_menu(message.chat.id)
#     elif message.text == "Active Broker":
#         selected_provider = "EKTIV"
#         send_main_menu(message.chat.id)
    
#     # Проверка выбора основного меню
#     elif message.text == "Баланс" and selected_provider:
        
#         bot.send_message(message.chat.id, result_string(provider=selected_provider, type='BALANCE'))
    
#     elif message.text == "PNL" and selected_provider:
        
#         send_submenu(message.chat.id, "PNL")

#     elif message.text == "Equity" and selected_provider:
        
#         bot.send_message(message.chat.id, result_string(provider=selected_provider, type='EKVITY'))

#     # Обработка кнопки "Назад" для возврата к выбору провайдера
#     elif message.text == "Назад":
#         if selected_provider:
#             send_provider_choice(message)  # возвращение к выбору провайдера
#             selected_provider = None
#         else:
#             send_main_menu(message.chat.id)  # если не выбран провайдер, вернуться в главное меню

#     # Обработка выбора дат для PNL
#     elif message.text == "PNL - Сегодня" and selected_provider:
#         bot.send_message(message.chat.id, "Думаю...")
#         start, end = get_today()
#         bot.send_message(message.chat.id, f"Информация по PNL - Сегодня: {result_string(provider=selected_provider, type='PNL', start=start, end=end)}")
#     elif message.text == "PNL - Вчера" and selected_provider:
#         bot.send_message(message.chat.id, "Думаю...")
#         start, end = get_yesterday()
#         bot.send_message(message.chat.id, f"Информация по PNL - Вчера: {result_string(provider=selected_provider, type='PNL', start=start, end=end)}")
#     elif message.text == "PNL - Текущая неделя" and selected_provider:
#         bot.send_message(message.chat.id, "Думаю...")
#         start, end = get_week()
#         bot.send_message(message.chat.id, f"Информация по PNL - Текущая неделя: {result_string(provider=selected_provider, type='PNL', start=start, end=end)}")
#     elif message.text == "PNL - Текущий месяц" and selected_provider:
#         bot.send_message(message.chat.id, "Думаю...")
#         start, end = get_month()
#         bot.send_message(message.chat.id, f"Информация по PNL - Текущий месяц: {result_string(provider=selected_provider, type='PNL', start=start, end=end)}")

#     # Сообщение о необходимости выбора провайдера, если пользователь пропустил шаг
#     elif not selected_provider:
#         bot.send_message(message.chat.id, "Пожалуйста, сначала выберите провайдера, отправив команду /start.")
# import time
# import telebot
# from requests.exceptions import ConnectionError, Timeout

# def start_bot():
#     while True:
#         try:
#             print('Manager bot for MT5 started!')
#             bot.polling(none_stop=True)
        
#         # except Timeout as e:
#         #     # Обработка ошибки тайм-аута
#             bot.send_message(620211681, f"TimeoutError: {e}")
#         #     time.sleep(5)  # Даем 5 секунд на восстановление соединения
        
#         # except ConnectionError as e:
#         #     # Обработка ошибок подключения
#             bot.send_message(620211681, f"ConnectionError: {e}. Trying to reconnect...")
#         #     time.sleep(5)  # Даем 5 секунд на восстановление соединения

#         except Exception as e:
#             # Обработка любых других исключений
#             bot.send_message(620211681, f"Unexpected error: {e}")
#             time.sleep(5)  # Даем 5 секунд на восстановление соединения


# if __name__ == "__main__":
#     start_bot()




import pandas as pd
import datetime
from dop_files import result_string

from telebot.async_telebot import AsyncTeleBot
from telebot import types
import asyncio

KEY_BOT_MANGER_MT5 = '7840597904:AAHrwP2adJsCLSg3myhTDEW-eJ4gtujG-UU'
bot = AsyncTeleBot(KEY_BOT_MANGER_MT5)

# Глобальная переменная для хранения выбранного провайдера
selected_provider = None

# Обработчик команды /start
@bot.message_handler(commands=['start'])
async def send_provider_choice(message):
    # Создание клавиатуры для выбора провайдера
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    provider1_button = types.KeyboardButton("Neo MU")
    provider2_button = types.KeyboardButton("Active Broker")
    markup.add(provider1_button, provider2_button)
    
    # Отправка сообщения с выбором провайдера
    await bot.send_message(message.chat.id, "Выберите провайдера:", reply_markup=markup)

# Функция для создания основного меню после выбора провайдера
async def send_main_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Баланс")
    button2 = types.KeyboardButton("PNL")
    button3 = types.KeyboardButton("Equity")
    button4 = types.KeyboardButton("Назад")
    markup.add(button1, button2, button3, button4)
    
    await bot.send_message(chat_id, "Выберите опцию:", reply_markup=markup)

# Функция для создания подменю с кнопками дат
async def send_submenu(chat_id, main_option):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    sub_button1 = types.KeyboardButton(f"{main_option} - Сегодня")
    sub_button2 = types.KeyboardButton(f"{main_option} - Вчера")
    sub_button3 = types.KeyboardButton(f"{main_option} - Текущая неделя")
    sub_button4 = types.KeyboardButton(f"{main_option} - Текущий месяц")
    back_button = types.KeyboardButton("Назад")
    markup.add(sub_button1, sub_button2, sub_button3, sub_button4, back_button)
    await bot.send_message(chat_id, f"Вы выбрали {main_option}. Выберите период:", reply_markup=markup)

# Функции для получения нужных дат
def get_today():
    today = datetime.date.today().strftime('%Y-%m-%d')
    return today, today

def get_yesterday():
    yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    return yesterday, yesterday

def get_week():
    start_of_week = datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday())
    return start_of_week.strftime('%Y-%m-%d'), datetime.date.today().strftime('%Y-%m-%d')

def get_month():
    start_of_month = datetime.date.today().replace(day=1)
    return start_of_month.strftime('%Y-%m-%d'), datetime.date.today().strftime('%Y-%m-%d')

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
async def handle_message(message):
    global selected_provider

    # Проверка выбора провайдера
    if message.text == "Neo MU":
        selected_provider = "NEO"
        await send_main_menu(message.chat.id)
    elif message.text == "Active Broker":
        selected_provider = "EKTIV"
        await send_main_menu(message.chat.id)
    
    # Проверка выбора основного меню
    elif message.text == "Баланс" and selected_provider:
        await bot.send_message(message.chat.id, result_string(provider=selected_provider, type='BALANCE'))
    
    elif message.text == "PNL" and selected_provider:
        await send_submenu(message.chat.id, "PNL")

    elif message.text == "Equity" and selected_provider:
        await bot.send_message(message.chat.id, result_string(provider=selected_provider, type='EKVITY'))

    # Обработка кнопки "Назад" для возврата к выбору провайдера
    elif message.text == "Назад":
        if selected_provider:
            await send_provider_choice(message)  # возвращение к выбору провайдера
            selected_provider = None
        else:
            await send_main_menu(message.chat.id)  # если не выбран провайдер, вернуться в главное меню

    # Обработка выбора дат для PNL
    elif message.text == "PNL - Сегодня" and selected_provider:
        await bot.send_message(message.chat.id, "Думаю...")
        start, end = get_today()
        await bot.send_message(message.chat.id, f"Информация по PNL - Сегодня: {result_string(provider=selected_provider, type='PNL', start=start, end=end)}")
    elif message.text == "PNL - Вчера" and selected_provider:
        await bot.send_message(message.chat.id, "Думаю...")
        start, end = get_yesterday()
        await bot.send_message(message.chat.id, f"Информация по PNL - Вчера: {result_string(provider=selected_provider, type='PNL', start=start, end=end)}")
    elif message.text == "PNL - Текущая неделя" and selected_provider:
        await bot.send_message(message.chat.id, "Думаю...")
        start, end = get_week()
        await bot.send_message(message.chat.id, f"Информация по PNL - Текущая неделя: {result_string(provider=selected_provider, type='PNL', start=start, end=end)}")
    elif message.text == "PNL - Текущий месяц" and selected_provider:
        await bot.send_message(message.chat.id, "Думаю...")
        start, end = get_month()
        await bot.send_message(message.chat.id, f"Информация по PNL - Текущий месяц: {result_string(provider=selected_provider, type='PNL', start=start, end=end)}")

    # Если провайдер не выбран, просим выбрать его
    elif not selected_provider:
        await bot.send_message(message.chat.id, "Пожалуйста, сначала выберите провайдера, отправив команду /start.")

# Асинхронный запуск бота с обработкой исключений
async def start_bot():
    while True:
        try:
            print('Manager bot for MT5 started!')
            await bot.polling(none_stop=True)
        except Exception as e:
            await bot.send_message(620211681, f"Unexpected error: {e}")
            await asyncio.sleep(5)  # Пауза 5 секунд перед повторным запуском
        
import sys
if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

if __name__ == "__main__":
    asyncio.run(start_bot())

