import pandas as pd
import datetime
from dop_files import result_string
from new_dop_files import PNL_get, balance_and_E
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
    button1 = types.KeyboardButton("Баланс и Equity")
    button2 = types.KeyboardButton("PNL")
    button4 = types.KeyboardButton("Назад")
    markup.add(button1, button2, button4)
    
    await bot.send_message(chat_id, "Выберите опцию:", reply_markup=markup)

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
    elif message.text == "Баланс и Equity" and selected_provider:
        await bot.send_message(message.chat.id, balance_and_E(broker=selected_provider),  parse_mode='Markdown')
       
    
    elif message.text == "PNL" and selected_provider:
        await bot.send_message(message.chat.id, 'Получаем данные...')
        await bot.send_message(message.chat.id, PNL_get(broker=selected_provider),  parse_mode='Markdown')
      

    # Обработка кнопки "Назад" для возврата к выбору провайдера
    elif message.text == "Назад":
        if selected_provider:
            await send_provider_choice(message)  # возвращение к выбору провайдера
            selected_provider = None
        else:
            await send_main_menu(message.chat.id)  # если не выбран провайдер, вернуться в главное меню


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

