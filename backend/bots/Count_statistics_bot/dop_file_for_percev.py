CONFIG_1 = {
    'user': 'neo_reports',
    'password': 'gh2uyti56hgk2h',
    'host': '92.38.186.22',
    'port': '3306',
    'raise_on_warnings': True
}
import warnings
import mysql.connector
connection = mysql.connector.connect(**CONFIG_1)
import datetime
warnings.filterwarnings("ignore")
import pandas as pd

from new_sql_qwer_Percev import Balanc, Equity, Realized_pnl


def get_today() -> tuple:
    """Возвращает сегодняшнюю дату в формате (start, end)."""
    today = datetime.date.today().strftime('%Y-%m-%d')
    return today, today


def get_yesterday() -> tuple:
    """Возвращает вчерашнюю дату в формате (start, end)."""
    yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    return yesterday, yesterday


def get_week() -> tuple:
    """Возвращает текущую неделю в формате (start, end)."""
    start_of_week = datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday())
    return start_of_week.strftime('%Y-%m-%d'), datetime.date.today().strftime('%Y-%m-%d')


def get_month() -> tuple:
    """Возвращает текущий месяц в формате (start, end)."""
    start_of_month = datetime.date.today().replace(day=1)
    return start_of_month.strftime('%Y-%m-%d'), datetime.date.today().strftime('%Y-%m-%d')


def get_azpros(zapros: str, start: str = None, end: str = None) -> str:
    """Выполняет SQL-запрос и возвращает результат как строку.

    Args:
        zapros (str): Тип запроса ('Equity', 'Realized_pnl', 'Balanc').
        start (str, optional): Начало периода для PNL.
        end (str, optional): Конец периода для PNL.

    Returns:
        str: Форматированный результат (например, 'Equity: 123.45').
    """
    connection = mysql.connector.connect(**CONFIG_1)
    dict_zap = {
        "Equity": Equity,
        "Realized_pnl": Realized_pnl(start=start, end=end),
        "Balanc": Balanc
    }

    df = pd.read_sql_query(dict_zap[zapros].replace("\\", "\\\\"), con=connection)
    d = dict(zip(df.columns, *df.values))
    connection.close()
    return f'{zapros}: {list(d.values())[0]}'