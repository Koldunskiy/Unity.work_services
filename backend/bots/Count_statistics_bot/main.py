
# from dop_file_for_percev import get_azpros, get_today, get_month, get_week, get_yesterday
# import telebot
# import schedule
# import time
# from telebot import types
# from dop_file import (count_all_accaunts, count_all_history_accaunts, build_graphs, validate_date_string,
#                        Total_Open_Positions, get_current_week, get_current_month, get_last_month,
#                        get_last_week, count_dayly_PNL_and_make_graphs, unrelizPNL, get_binance_balance, bybit_balance, get_dynamic_balance_bybit, margin_wallet)
# import matplotlib
# import datetime
# import sys
# import time
# from button import (create_user_menu, create_broker_menu, create_broker_menu_for_percev, create_main_menu,
#                     create_main_menu_for_MT5_Percev, create_menu_Select_time_interval, create_interval_menu,
#                      create_walet_binance, binace_traders, Bybit_traders, type_balnce_bybit)

# matplotlib.use('Agg')
# key = '7790293210:AAHxKy3OH1cTc5Z_t9wYDZVOrVN-Z6_cLBk'
# bot = telebot.TeleBot(key)
# Neo_MU_Key = '8c75f6a6-d3e6-4257-b6e5-4513f36975b9'
# Neo_KZ_Key = '08d238f9-2af9-4cd7-8d95-e0bcb2f050a8'
# ARK_Capital_Key = '41da8163-8e10-4b8d-be5e-9b01f3a7304d'

# Neo_MU_accaunts = [
#     1889,
#     2296,
#     2522,
#     2760,
#     3175,
#     5220,
#     5264, 
#     5662 # по идее основнй
# ]
# Neo_KZ_accaunts = [
#     3314,
#     3315,
#     3316,
#     4769
# ]

# ARK_Capital_accaunts = [4976]

# Unity_Server_percev_accaunts = [5242, 5243]

# hist_message = False
# type_message = None
# accaunts = None
# headers = None






# @bot.message_handler(commands=['start'])
# def start_message(message):
#     bot.send_message(
#         message.chat.id,
#         "Привет! Выбери пользователя:",
#         reply_markup=create_user_menu()
#     )



# def handle_interval_selection(chat_id, action_type, time_start, time_end):
#     if action_type == 'balance':
#         data = count_all_history_accaunts(headers, accaunts, time_start, time_end)
#         # print(data)
#         prices = (list(data.tolist()))
#         prices_str = (str(prices)).replace('[', '').replace(']', '')
#         message_to_send = f'''
# Total Balance: {sum(prices):.2f} USD
# Balance by day: {prices_str}
# '''
#         bot.send_message(chat_id, message_to_send)
#         build_graphs(data)
#         with open("graph.png", "rb") as file:
#             bot.send_photo(chat_id, file)
#     elif action_type == 'pnl':
        
#         total_sum = count_dayly_PNL_and_make_graphs(headers, accaunts, time_start, time_end)
#         # print(total_sum)
#         bot.send_message(chat_id, f"Total Profit: {total_sum:.2f} USD")
#         with open("graph2.png", "rb") as file:
#             bot.send_photo(chat_id, file)



#     # print(message.chat.id)

# @bot.message_handler(func=lambda message: message.text == "Anton")
# def select_broker(message):
#     global message_id
#     message_id = message.chat.id
#     bot.send_message(message.chat.id, "Выбери брокера:", reply_markup=create_broker_menu())

    
# @bot.message_handler(func=lambda message: message.text == "Percev")
# def select_broker(message):
#     global message_id
#     message_id = message.chat.id
#     bot.send_message(message.chat.id, "Выбери брокера:", reply_markup=create_broker_menu_for_percev())
# # Функция создания меню выбора интервала
    
# @bot.message_handler(func=lambda message: message.text == "Binance") #!!!
# def select_broker(message):
#     global message_id
#     message_id = message.chat.id
#     bot.send_message(message.chat.id, "Выбери трейдера:", reply_markup=binace_traders())

# @bot.message_handler(func=lambda message: message.text in ["Гвидо 1", "Гвидо 2", "Петр"]) #!!!
# def select_broker(message):
#     global binance_trader_name
   
#     if  message.text == 'Гвидо 1':
#         binance_trader_name = 'Гвидо 1'
#     elif  message.text == 'Гвидо 2':
#         binance_trader_name = 'Гвидо 2'
#     else:
#         binance_trader_name = 'Петр'

#     bot.send_message(message.chat.id, "Выберите счет:", reply_markup=create_walet_binance()) #!!!



# @bot.message_handler(func=lambda message: message.text in ['FUTURES', "SPOT", 'MARGIN'])
# def select_broker(message):
#     global message_id
#     message_id = message.chat.id

#     if message.text == 'FUTURES':
#         ansvwer = get_binance_balance(30, 'FUTURES', binance_trader_name)
#     if message.text == 'SPOT':
#         ansvwer = get_binance_balance(30, 'SPOT', binance_trader_name)
#     if message.text == 'MARGIN':
#         ansvwer = get_binance_balance(30, 'MARGIN', binance_trader_name)

#     if message.text != 'MARGIN':
#         try:
#             with open("Binance_walet.png", "rb") as file:
#                 bot.send_photo(message.chat.id, file)
#         except Exception as e:
#             bot.send_photo(message.chat.id, e)
            
#     bot.send_message(message.chat.id, ansvwer)
  

# #Bybit
# @bot.message_handler(func=lambda message: message.text == "Bybit") #!!!
# def select_broker(message):
#     global message_id
#     message_id = message.chat.id
#     bot.send_message(message.chat.id, "Выбери трейдера:", reply_markup=Bybit_traders())

# @bot.message_handler(func=lambda message: message.text == "Андрей") #!!!
# def select_broker(message):
#     global message_id
#     message_id = message.chat.id
#     bot.send_message(message.chat.id, "Выбери тип запроса:", reply_markup=type_balnce_bybit())

# @bot.message_handler(func=lambda message: message.text in ["Баланс Bybit", "Динамика баланса Bybit"]) #!!!
# def select_broker(message):
#     global message_id
#     message_id = message.chat.id
#     if message.text == "Баланс Bybit":
#         answer = bybit_balance()
#         bot.send_message(message.chat.id, answer)
#     if message.text == "Динамика баланса Bybit":
#         answer = get_dynamic_balance_bybit()
#         with open("Binance_walet.png", "rb") as file:
#             bot.send_photo(message.chat.id, file)
#         bot.send_message(message.chat.id, answer)
        


        
# @bot.message_handler(func=lambda message: message.text == "MT 5")
# def select_broker(message):
#     bot.send_message(message.chat.id, "Выбери брокера:", reply_markup=create_main_menu_for_MT5_Percev())

# @bot.message_handler(func=lambda message: message.text in ["Equity", 'Realized_pnl', 'Balanc'])
# def broker_selection(message):
#     if message.text == "Equity":
#         bot.send_message(message.chat.id, 'Думаю...')
#         result_string = get_azpros(zapros="Equity")
#         bot.send_message(message.chat.id, result_string)
#     if message.text == "Realized_pnl":
#         bot.send_message(message.chat.id, "Выбери временной интервал:", reply_markup=create_menu_Select_time_interval())
#     if message.text == "Balanc":
#         bot.send_message(message.chat.id, 'Думаю...')
#         result_string = get_azpros(zapros="Balanc")
#         bot.send_message(message.chat.id, result_string)
#     #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# @bot.message_handler(func=lambda message: message.text in ["Сегодня", 'Вчера', 'Неделя', "Месяц"])
# def broker_selection(message):
#     if message.text == "Сегодня":
#         start, end = get_today()
#     if message.text == "Вчера":
#         start, end = get_yesterday()
#     if message.text == "Неделя":
#         start, end = get_week()
#     if message.text == "Месяц":
#         start, end = get_month()
    
#     bot.send_message(message.chat.id, 'Думаю...')
#     result_string = get_azpros(zapros="Realized_pnl", start=start, end=end)
#     bot.send_message(message.chat.id, result_string)

    

# @bot.message_handler(func=lambda message: message.text in ["Другой пользователь"])
# def other_user(message):
#     bot.send_message(message.chat.id, "Данный сервис временно недоступен.", reply_markup=create_user_menu())

# @bot.message_handler(func=lambda message: message.text in ["Neo MU", "Neo KZ", 'ARK', "Unity Server"])
# def broker_selection(message):
#     global accaunts, headers, type_broker
#     if message.text == "Neo MU":
#         type_broker = 'Neo MU'
#         accaunts = Neo_MU_accaunts
#         headers = {'accept': 'application/json', 'auth-token': Neo_MU_Key}
#     elif message.text == "Neo KZ":
#         type_broker = 'Neo KZ'
#         accaunts = Neo_KZ_accaunts
#         headers = {'accept': 'application/json', 'auth-token': Neo_KZ_Key}
#     elif message.text == "ARK":
#         type_broker = 'ARK'
#         accaunts = ARK_Capital_accaunts
#         headers = {'accept': 'application/json', 'auth-token': ARK_Capital_Key}
#     elif message.text == "Unity Server":
#         type_broker = 'Unity Server'
#         accaunts = Unity_Server_percev_accaunts
#         headers = {'accept': 'application/json', 'auth-token': Neo_MU_Key}
    
#     bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=create_main_menu())

# @bot.message_handler(func=lambda message: message.text in ["Дневной PnL", "Balance dynamic", "PnL dynamic"])
# def main_menu_handler(message):
#     global type_message
#     if message.text == "Дневной PnL":
#         bot.send_message(message.chat.id, 'Думаю...')
#         totalAssets, prevTotalAssets = count_all_accaunts(headers, accaunts)
#         unPNl = unrelizPNL(headers, accaunts)
#         bot.send_message(message.chat.id, f'''Broker: {type_broker}
# Accounts: {', '.join(map(str, accaunts))}
# Date: {datetime.datetime.now().strftime('%d-%m-%Y')}
# Total Balance (Assets): {totalAssets:,.2f} USD
# Released PnL (Day): {(totalAssets - prevTotalAssets):,.2f} USD
# Total Open Positions: {Total_Open_Positions(headers, accaunts):,.2f} USD
# UnReleased PnL: {unPNl:,.2f} USD'''.replace(',', ' '))
        
#     elif message.text == "Balance dynamic":
#         bot.send_message(message.chat.id, "Выбери временной интервал:", reply_markup=create_interval_menu())
#         type_message = 'balance'

#     elif message.text == "PnL dynamic":
#         bot.send_message(message.chat.id, "Выбери временной интервал:", reply_markup=create_interval_menu())
#         type_message = 'pnl'

# @bot.message_handler(func=lambda message: message.text == "Назад")
# def back_to_main_menu(message):
#     bot.send_message(message.chat.id, "Выбери пользователя:", reply_markup=create_user_menu())

# # Обработка других сообщений и действий можно добавить здесь
#     # Обработчик кнопок временных интервалов
# @bot.message_handler(func=lambda message: message.text in ["Текущая неделя", "Прошлая неделя", "Текущий месяц", "Прошлый месяц", "Кастомный интервал"])
# def interval_menu_handler(message):
#     global type_message, hist_message
#     if message.text == "Кастомный интервал":
#         bot.send_message(message.chat.id, "Отправь временной интервал в формате: dd-mm-yyyy, dd-mm-yyyy")
#         hist_message = True
#     else:
#         if message.text == "Текущая неделя":
#             time_start, time_end = get_current_week()
#         elif message.text == "Прошлая неделя":
#             time_start, time_end = get_last_week()
#         elif message.text == "Текущий месяц":
#             time_start, time_end = get_current_month()
#         elif message.text == "Прошлый месяц":
#             time_start, time_end = get_last_month()

#         handle_interval_selection(message.chat.id, type_message, time_start, time_end)
#         type_message = None

# # Обработчик кастомного интервала
# @bot.message_handler(func=lambda message: hist_message)
# def custom_interval_handler(message):
#     global hist_message, type_message
#     if validate_date_string(message.text):
#         try:
#             date1_str, date2_str = message.text.split(',')
#             time_start = datetime.datetime.strptime(date1_str.strip(), "%d-%m-%Y").strftime("%Y-%m-%d")
#             time_end = datetime.datetime.strptime(date2_str.strip(), "%d-%m-%Y").strftime("%Y-%m-%d")

#             handle_interval_selection(message.chat.id, type_message, time_start, time_end)
#         except Exception as e:
#             bot.send_message(message.chat.id, f"Ошибка обработки данных: {e}")
#     else:
#         bot.send_message(message.chat.id, "Неправильный формат! Используй: dd-mm-yyyy, dd-mm-yyyy")
#     hist_message = False


# # Функция, которая будет выполняться ровно в 12:00 каждый день
# def my_function():
#     print("Функция выполнена в 12:00!")
#     # bot.send_message(message_id, "Функция выполнена в 12:00!")



# while True:
#     print('agg_accaunts_bot заработал!')
#     try:
#         # Пытаемся запустить polling
#         bot.polling(none_stop=True)
    
#     except ValueError as e:
#         # Обработка ValueError
#         bot.send_message(message_id, f"Ошибка ValueError: {e}")
#         time.sleep(2)  # Задержка перед перезапуском

#     except Exception as e:
#         # Обработка всех остальных ошибок
#         bot.send_message(message_id, f"Oшибка: {e}")
#         # print(f"Неизвестная ошибка: {e}")
#         # bot.send_message(message_id, f"Пожалуйста, обратитесь в службу поддержки! Приносим сердечные извинения 😔😔😔...")
#         time.sleep(2)  # Задержка перед перезапуском

#     except KeyboardInterrupt:
#         # Завершение работы при нажатии Ctrl+C
#         print("Бот остановлен пользователем")
#         sys.exit(0)

# # 620211681



from dop_file_for_percev import get_azpros, get_today, get_month, get_week, get_yesterday
import telebot.async_telebot as async_telebot
import schedule
import time
from telebot import types
from dop_file import (
    count_all_accaunts, count_all_history_accaunts, build_graphs, validate_date_string,
    Total_Open_Positions, get_current_week, get_current_month, get_last_month,
    get_last_week, count_dayly_PNL_and_make_graphs, unrelizPNL, get_binance_balance,
    bybit_balance, get_dynamic_balance_bybit, margin_wallet
)
import matplotlib
import datetime
import sys
import time
from button import (
    create_user_menu, create_broker_menu, create_broker_menu_for_percev, create_main_menu,
    create_main_menu_for_MT5_Percev, create_menu_Select_time_interval, create_interval_menu,
    create_walet_binance, binace_traders, Bybit_traders, type_balnce_bybit
)

matplotlib.use('Agg')
key = '7790293210:AAHxKy3OH1cTc5Z_t9wYDZVOrVN-Z6_cLBk'
bot = async_telebot.AsyncTeleBot(key)

Neo_MU_Key = '8c75f6a6-d3e6-4257-b6e5-4513f36975b9'
Neo_KZ_Key = '08d238f9-2af9-4cd7-8d95-e0bcb2f050a8'
ARK_Capital_Key = '41da8163-8e10-4b8d-be5e-9b01f3a7304d'

Neo_MU_accaunts = [1889, 2296, 2522, 2760, 3175, 5220, 5264, 5662]  # по идее основной
Neo_KZ_accaunts = [3314, 3315, 3316, 4769]
ARK_Capital_accaunts = [4976]
Unity_Server_percev_accaunts = [5242, 5243]

hist_message = False
type_message = None
accaunts = None
headers = None
message_id = None
binance_trader_name = None

# Асинхронная функция-обработчик команды /start
@bot.message_handler(commands=['start'])
async def start_message(message):
    await bot.send_message(
        message.chat.id,
        "Привет! Выбери пользователя:",
        reply_markup=create_user_menu()
    )

# Асинхронная функция для отправки сообщений и фотографий (работа с Telegram)
async def handle_interval_selection(chat_id, action_type, time_start, time_end):
    if action_type == 'balance':
        data = count_all_history_accaunts(headers, accaunts, time_start, time_end)
        prices = list(data.tolist())
        prices_str = str(prices).replace('[', '').replace(']', '')
        message_to_send = f'''
Total Balance: {sum(prices):.2f} USD
Balance by day: {prices_str}
'''
        await bot.send_message(chat_id, message_to_send)
        build_graphs(data)
        with open("graph.png", "rb") as file:
            await bot.send_photo(chat_id, file)
    elif action_type == 'pnl':
        total_sum = count_dayly_PNL_and_make_graphs(headers, accaunts, time_start, time_end)
        await bot.send_message(chat_id, f"Total Profit: {total_sum:.2f} USD")
        with open("graph2.png", "rb") as file:
            await bot.send_photo(chat_id, file)

# Обработчик для пользователя "Anton"
@bot.message_handler(func=lambda message: message.text == "Anton")
async def handle_anton(message):
    global message_id
    message_id = message.chat.id
    await bot.send_message(message.chat.id, "Выбери брокера:", reply_markup=create_broker_menu())

# Обработчик для пользователя "Percev"
@bot.message_handler(func=lambda message: message.text == "Percev")
async def handle_percev(message):
    global message_id
    message_id = message.chat.id
    await bot.send_message(message.chat.id, "Выбери брокера:", reply_markup=create_broker_menu_for_percev())

# Обработчик для выбора брокера "Binance"
@bot.message_handler(func=lambda message: message.text == "Binance")
async def handle_binance(message):
    global message_id
    message_id = message.chat.id
    await bot.send_message(message.chat.id, "Выбери трейдера:", reply_markup=binace_traders())

# Обработчик для выбора трейдера Binance ("Гвидо 1", "Гвидо 2", "Петр")
@bot.message_handler(func=lambda message: message.text in ["Гвидо 1", "Гвидо 2", "Петр"])
async def handle_binance_trader(message):
    global binance_trader_name
    if message.text == 'Гвидо 1':
        binance_trader_name = 'Гвидо 1'
    elif message.text == 'Гвидо 2':
        binance_trader_name = 'Гвидо 2'
    else:
        binance_trader_name = 'Петр'
    await bot.send_message(message.chat.id, "Выберите счет:", reply_markup=create_walet_binance())

# Обработчик для выбора типа счета Binance (FUTURES, SPOT, MARGIN)
@bot.message_handler(func=lambda message: message.text in ['FUTURES', "SPOT", 'MARGIN'])
async def handle_binance_account_type(message):
    global message_id
    message_id = message.chat.id
    try:
        if message.text == 'FUTURES':
            ansvwer = get_binance_balance(30, 'FUTURES', binance_trader_name)
        elif message.text == 'SPOT':
            ansvwer = get_binance_balance(30, 'SPOT', binance_trader_name)
        elif message.text == 'MARGIN':
            ansvwer = get_binance_balance(30, 'MARGIN', binance_trader_name)
        ansvwer = str(ansvwer)
        await bot.send_message(message.chat.id, ansvwer)
    except Exception as e:
        await bot.send_message(message.chat.id, f"Ошибка: {e}")
        return

    if message.text != 'MARGIN':
        try:
            with open("Binance_walet.png", "rb") as file:
                await bot.send_photo(message.chat.id, file)
        except Exception as e:
            await bot.send_photo(message.chat.id, str(e))


# Обработчик для выбора брокера "Bybit"
@bot.message_handler(func=lambda message: message.text == "Bybit")
async def handle_bybit(message):
    global message_id
    message_id = message.chat.id
    await bot.send_message(message.chat.id, "Выбери трейдера:", reply_markup=Bybit_traders())

# Обработчик для выбора трейдера Bybit ("Андрей")
@bot.message_handler(func=lambda message: message.text == "Андрей")
async def handle_bybit_andrey(message):
    global message_id
    message_id = message.chat.id
    await bot.send_message(message.chat.id, "Выбери тип запроса:", reply_markup=type_balnce_bybit())

# Обработчик для запроса по балансам и динамике баланса Bybit
@bot.message_handler(func=lambda message: message.text in ["Баланс Bybit", "Динамика баланса Bybit"])
async def handle_bybit_balance(message):
    global message_id
    message_id = message.chat.id
    if message.text == "Баланс Bybit":
        answer = bybit_balance()
        await bot.send_message(message.chat.id, answer)
    elif message.text == "Динамика баланса Bybit":
        answer = get_dynamic_balance_bybit()
        with open("Binance_walet.png", "rb") as file:
            await bot.send_photo(message.chat.id, file)
        await bot.send_message(message.chat.id, answer)

# Обработчик для выбора "MT 5"
@bot.message_handler(func=lambda message: message.text == "MT 5")
async def handle_MT5(message):
    await bot.send_message(message.chat.id, "Выбери брокера:", reply_markup=create_main_menu_for_MT5_Percev())

# Обработчик для запросов "Equity", "Realized_pnl", "Balanc"
@bot.message_handler(func=lambda message: message.text in ["Equity", 'Realized_pnl', 'Balanc'])
async def handle_MT5_broker_selection(message):
    if message.text == "Equity":
        await bot.send_message(message.chat.id, 'Думаю...')
        result_string = get_azpros(zapros="Equity")
        await bot.send_message(message.chat.id, result_string)
    elif message.text == "Realized_pnl":
        await bot.send_message(message.chat.id, "Выбери временной интервал:", reply_markup=create_menu_Select_time_interval())
    elif message.text == "Balanc":
        await bot.send_message(message.chat.id, 'Думаю...')
        result_string = get_azpros(zapros="Balanc")
        await bot.send_message(message.chat.id, result_string)

# Обработчик для выбора временного интервала по датам ("Сегодня", "Вчера", "Неделя", "Месяц")
@bot.message_handler(func=lambda message: message.text in ["Сегодня", 'Вчера', 'Неделя', "Месяц"])
async def handle_date_selection(message):
    if message.text == "Сегодня":
        start, end = get_today()
    elif message.text == "Вчера":
        start, end = get_yesterday()
    elif message.text == "Неделя":
        start, end = get_week()
    elif message.text == "Месяц":
        start, end = get_month()
    await bot.send_message(message.chat.id, 'Думаю...')
    result_string = get_azpros(zapros="Realized_pnl", start=start, end=end)
    await bot.send_message(message.chat.id, result_string)

# Обработчик для выбора "Другой пользователь"
@bot.message_handler(func=lambda message: message.text in ["Другой пользователь"])
async def handle_other_user(message):
    await bot.send_message(message.chat.id, "Данный сервис временно недоступен.", reply_markup=create_user_menu())

# Обработчик для выбора брокера ("Neo MU", "Neo KZ", "ARK", "Unity Server")
@bot.message_handler(func=lambda message: message.text in ["Neo MU", "Neo KZ", 'ARK', "Unity Server"])
async def handle_broker_selection(message):
    global accaunts, headers, type_broker
    if message.text == "Neo MU":
        type_broker = 'Neo MU'
        accaunts = Neo_MU_accaunts
        headers = {'accept': 'application/json', 'auth-token': Neo_MU_Key}
    elif message.text == "Neo KZ":
        type_broker = 'Neo KZ'
        accaunts = Neo_KZ_accaunts
        headers = {'accept': 'application/json', 'auth-token': Neo_KZ_Key}
    elif message.text == "ARK":
        type_broker = 'ARK'
        accaunts = ARK_Capital_accaunts
        headers = {'accept': 'application/json', 'auth-token': ARK_Capital_Key}
    elif message.text == "Unity Server":
        type_broker = 'Unity Server'
        accaunts = Unity_Server_percev_accaunts
        headers = {'accept': 'application/json', 'auth-token': Neo_MU_Key}
    await bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=create_main_menu())

# Обработчик для основных запросов ("Дневной PnL", "Balance dynamic", "PnL dynamic")
@bot.message_handler(func=lambda message: message.text in ["Дневной PnL", "Balance dynamic", "PnL dynamic"])
async def handle_main_menu(message):
    global type_message
    if message.text == "Дневной PnL":
        await bot.send_message(message.chat.id, 'Думаю...')
        totalAssets, prevTotalAssets = count_all_accaunts(headers, accaunts)
        unPNl = unrelizPNL(headers, accaunts)
        await bot.send_message(
            message.chat.id,
            f'''Broker: {type_broker}
Accounts: {', '.join(map(str, accaunts))}
Date: {datetime.datetime.now().strftime('%d-%m-%Y')}
Total Balance (Assets): {totalAssets:,.2f} USD
Released PnL (Day): {(totalAssets - prevTotalAssets):,.2f} USD
Total Open Positions: {Total_Open_Positions(headers, accaunts):,.2f} USD
UnReleased PnL: {unPNl:,.2f} USD'''.replace(',', ' ')
        )
    elif message.text == "Balance dynamic":
        await bot.send_message(message.chat.id, "Выбери временной интервал:", reply_markup=create_interval_menu())
        type_message = 'balance'
    elif message.text == "PnL dynamic":
        await bot.send_message(message.chat.id, "Выбери временной интервал:", reply_markup=create_interval_menu())
        type_message = 'pnl'

# Обработчик для команды "Назад"
@bot.message_handler(func=lambda message: message.text == "Назад")
async def handle_back(message):
    await bot.send_message(message.chat.id, "Выбери пользователя:", reply_markup=create_user_menu())

# Обработчик для кнопок выбора временного интервала
@bot.message_handler(func=lambda message: message.text in ["Текущая неделя", "Прошлая неделя", "Текущий месяц", "Прошлый месяц", "Кастомный интервал"])
async def handle_interval_menu(message):
    global type_message, hist_message
    if message.text == "Кастомный интервал":
        await bot.send_message(message.chat.id, "Отправь временной интервал в формате: dd-mm-yyyy, dd-mm-yyyy")
        hist_message = True
    else:
        if message.text == "Текущая неделя":
            time_start, time_end = get_current_week()
        elif message.text == "Прошлая неделя":
            time_start, time_end = get_last_week()
        elif message.text == "Текущий месяц":
            time_start, time_end = get_current_month()
        elif message.text == "Прошлый месяц":
            time_start, time_end = get_last_month()
        await handle_interval_selection(message.chat.id, type_message, time_start, time_end)
        type_message = None

# Обработчик для кастомного временного интервала
@bot.message_handler(func=lambda message: hist_message)
async def handle_custom_interval(message):
    global hist_message, type_message
    if validate_date_string(message.text):
        try:
            date1_str, date2_str = message.text.split(',')
            time_start = datetime.datetime.strptime(date1_str.strip(), "%d-%m-%Y").strftime("%Y-%m-%d")
            time_end = datetime.datetime.strptime(date2_str.strip(), "%d-%m-%Y").strftime("%Y-%m-%d")
            await handle_interval_selection(message.chat.id, type_message, time_start, time_end)
        except Exception as e:
            await bot.send_message(message.chat.id, f"Ошибка обработки данных: {e}")
    else:
        await bot.send_message(message.chat.id, "Неправильный формат! Используй: dd-mm-yyyy, dd-mm-yyyy")
    hist_message = False



# Основной цикл запуска бота с обработкой исключений
import asyncio

async def main():
    while True:
        print('agg_accaunts_bot заработал!')
        try:
            await bot.infinity_polling()
        except ValueError as e:
            await bot.send_message(message_id, f"Ошибка ValueError: {e}")
            await asyncio.sleep(2)
        except Exception as e:
            await bot.send_message(message_id, f"Oшибка: {e}")
            await asyncio.sleep(2)
        except KeyboardInterrupt:
            print("Бот остановлен пользователем")
            sys.exit(0)

import sys
if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

if __name__ == '__main__':
    asyncio.run(main())




