import telebot
from telebot import types


def create_user_menu() -> types.ReplyKeyboardMarkup:
    """Создаёт меню выбора пользователя."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_anton = types.KeyboardButton("Anton")
    button_percev = types.KeyboardButton("Percev")
    button_binance = types.KeyboardButton("Binance")
    button_bybit = types.KeyboardButton("Bybit")
    button_other = types.KeyboardButton("Другой пользователь")
    markup.add(button_anton, button_percev, button_binance)
    markup.add(button_bybit, button_other)
    return markup


def create_broker_menu() -> types.ReplyKeyboardMarkup:
    """Создаёт меню выбора брокера."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_neo = types.KeyboardButton("Neo MU")
    button_kz = types.KeyboardButton("Neo KZ")
    button_ark = types.KeyboardButton("ARK")
    button_back = types.KeyboardButton("Назад")
    markup.add(button_neo, button_kz, button_ark, button_back)
    return markup


def create_broker_menu_for_percev() -> types.ReplyKeyboardMarkup:
    """Создаёт меню брокера для Percev."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_unity = types.KeyboardButton("Unity Server")
    button_MT = types.KeyboardButton("MT 5")
    button_back = types.KeyboardButton("Назад")
    markup.add(button_unity, button_MT, button_back)
    return markup


def create_main_menu() -> types.ReplyKeyboardMarkup:
    """Создаёт основное меню."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Дневной PnL")
    button2 = types.KeyboardButton("Balance dynamic")
    button3 = types.KeyboardButton("PnL dynamic")
    button_back = types.KeyboardButton("Назад")
    markup.add(button1, button2, button3, button_back)
    return markup


def create_main_menu_for_MT5_Percev() -> types.ReplyKeyboardMarkup:
    """Создаёт меню для MT5 Percev."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Equity")
    button2 = types.KeyboardButton("Realized_pnl")
    button3 = types.KeyboardButton("Balanc")
    button_back = types.KeyboardButton("Назад")
    markup.add(button1, button2, button3, button_back)
    return markup


def create_menu_Select_time_interval() -> types.ReplyKeyboardMarkup:
    """Создаёт меню выбора интервала времени."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Сегодня")
    button2 = types.KeyboardButton("Вчера")
    button3 = types.KeyboardButton("Неделя")
    button4 = types.KeyboardButton("Месяц")
    button_back = types.KeyboardButton("Назад")
    markup.add(button1, button2, button3, button4, button_back)
    return markup


def create_interval_menu() -> types.ReplyKeyboardMarkup:
    """Создаёт меню детального интервала."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_week = types.KeyboardButton("Текущая неделя")
    button_last_week = types.KeyboardButton("Прошлая неделя")
    button_month = types.KeyboardButton("Текущий месяц")
    button_last_month = types.KeyboardButton("Прошлый месяц")
    button_custom = types.KeyboardButton("Кастомный интервал")
    button_back = types.KeyboardButton("Назад")
    markup.add(button_week, button_last_week)
    markup.add(button_month, button_last_month, button_custom)
    markup.add(button_back)
    return markup


def binace_traders(resize_keyboard: bool = True) -> types.ReplyKeyboardMarkup:
    """Создаёт меню трейдеров Binance."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=resize_keyboard)
    traders_1 = types.KeyboardButton("Гвидо 1")
    traders_2 = types.KeyboardButton("Гвидо 2")
    traders_3 = types.KeyboardButton("Петр")
    markup.add(traders_1, traders_2, traders_3)
    return markup


def create_walet_binance() -> types.ReplyKeyboardMarkup:
    """Создаёт меню типов кошельков Binance."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_future = types.KeyboardButton("FUTURES")
    button_spot = types.KeyboardButton("SPOT")
    button_margin = types.KeyboardButton("MARGIN")
    button_back = types.KeyboardButton("Назад")
    markup.add(button_future, button_spot, button_margin, button_back)
    return markup


def Bybit_traders() -> types.ReplyKeyboardMarkup:
    """Создаёт меню трейдеров Bybit."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_andrey = types.KeyboardButton("Андрей")
    markup.add(button_andrey)
    return markup


def type_balnce_bybit() -> types.ReplyKeyboardMarkup:
    """Создаёт меню типов баланса Bybit."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    balance = types.KeyboardButton("Баланс Bybit")
    balance_dinamic = types.KeyboardButton("Динамика баланса Bybit")
    button_back = types.KeyboardButton("Назад")
    markup.add(balance, balance_dinamic, button_back)
    return markup