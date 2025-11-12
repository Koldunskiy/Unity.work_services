
import pandas as pd
import warnings
import mysql.connector


from datetime import datetime
warnings.filterwarnings("ignore")
def get_formatted_date_time():
    # Получение текущей даты и времени
    now = datetime.now()
    # Форматирование даты и времени в нужном формате
    formatted_date_time = now.strftime("%d:%m:%Y")
    return formatted_date_time
from SQL_QUERY import get_sql_query

def result_string(provider:str, type:str, start:str=None, end:str=None) -> str:
    try:
        CONFIG_1 = {
        'user': 'neo_reports',
        'password': 'gh2uyti56hgk2h',
        'host': '92.38.186.22',
        'port': '3306',
        'raise_on_warnings': True
    }
        connection = mysql.connector.connect(**CONFIG_1)
        zapros = f'{provider}_{type}'.upper()
        zapros = get_sql_query(zapros, start, end).replace("\\", "\\\\")
        df = pd.read_sql_query(zapros, con=connection)
        if type == "BALANCE" and provider == 'EKTIV':
            result = f"Active Broker баланс : {df['total_balance_USD'].iloc[0]:,.2f} USD".replace(',', ' ')

        elif type == "EKVITY" and provider == 'EKTIV':
            result = f"Active Broker equity : {df['total_equity_s_credit_USD'].iloc[0]:,.2f} USD".replace(',', ' ')
        
        # elif type == "EKVITY" and provider == 'NEO':
        #     result = f"Neo MU  equity : {df['total_equity_s_credit_USD'].iloc[0]:,.2f} USD".replace(',', ' ')

        else:
            abook_value = df.T[df.T.index.str.contains('ABOOK')][0].values[0]
            bbook_value = df.T[df.T.index.str.contains('BBOOK') & ~df.T.index.str.contains('Cent_BBOOK')][0].values[0]
            cbook_value = df.T[df.T.index.str.contains('CBOOK')][0].values[0]
            cent_bbook_value = df.T[df.T.index.str.contains('Cent_BBOOK')][0].values[0] 
            # Cent_BBOOK = df.T[df.T.index.str.contains('Cent_BBOOK')][0].values[0] / 100
            if type == "EKVITY" and provider == 'NEO':
                total_book_value = df['total_equity_s_credit_USD'].iloc[0]
            else:

                if start == None:
                    start = get_formatted_date_time()
                    end = start
                if provider.upper() == 'EKTIV':
                    provider = 'Active Broker'
                    total_book_value = df.T[0].sum()

                if provider.upper() == 'NEO':
                    provider = 'Neo MU'
                    try:
                        total_book_value = df.T[df.T.index.str.contains('total_balance_USD')][0].values[0]
                    except:
                        total_book_value = df['Total_PnL_USD_side_client_realized'].iloc[0]

            result =  (f'''
Дата: {start} : {end}
Брокер: {provider}
Тип запроса: {type}

ABOOK: {abook_value:,.2f} USD
BBOOK: {bbook_value:,.2f} USD
CBOOK: {cbook_value:,.2f} USD
Cent BBOOK: {cent_bbook_value:,.2f} USD

Total {type}: {total_book_value:,.2f} USD
        '''.replace(',', ' '))
            connection.close()
        return result
    except Exception as e:
        raise TimeoutError(f"Не могу подключиться к БД. Проблемы с сетью. {e}")



# start, end = '2025-01-22', '2025-01-24'
# r = result_string(provider='NEO', type='EKVITY', start=start, end=end) 

# print(r)





# import pandas as pd
# import warnings
# import pymysql  # Импортируем pymysql

# from datetime import datetime
# warnings.filterwarnings("ignore")

# def get_formatted_date_time():
#     # Получение текущей даты и времени
#     now = datetime.now()
#     # Форматирование даты и времени в нужном формате
#     formatted_date_time = now.strftime("%d:%m:%Y")
#     return formatted_date_time

# from SQL_QUERY import get_sql_query

# def result_string(provider: str, type: str, start: str = None, end: str = None) -> str:
#     CONFIG_1 = {
#         'user': 'neo_reports',
#         'password': 'gh2uyti56hgk2h',
#         'host': '92.38.186.22',
#         'port': 3306,  # Порт по умолчанию для MySQL
#         'database': 'your_database_name',  # Замените на нужное имя базы данных
#         'cursorclass': pymysql.cursors.DictCursor  # Используем словарный курсор для удобства
#     }

#     # Устанавливаем соединение с базой данных
#     connection = pymysql.connect(**CONFIG_1)
    
#     try:
#         zapros = f'{provider}_{type}'.upper()  # Формируем запрос
#         zapros = get_sql_query(zapros, start, end).replace("\\", "\\\\")  # Получаем SQL запрос
#         # Выполняем запрос и получаем данные в DataFrame
#         df = pd.read_sql_query(zapros, con=connection)

#         # Извлекаем значения для каждого типа книги
#         abook_value = df.T[df.T.index.str.contains('ABOOK')][0].values[0]
#         bbook_value = df.T[df.T.index.str.contains('BBOOK') & ~df.T.index.str.contains('Cent_BBOOK')][0].values[0]
#         cbook_value = df.T[df.T.index.str.contains('CBOOK')][0].values[0]
#         cent_bbook_value = df.T[df.T.index.str.contains('Cent_BBOOK')][0].values[0] / 100

#         # Если start и end не переданы, используем текущую дату
#         if start is None:
#             start = get_formatted_date_time()
#             end = start

#         # Формируем итоговую строку
#         result = (f'''
# Дата: {start} : {end}
# Провайдер: {provider.upper()}
# Тип запроса: {type}

# ABOOK: {abook_value:,.3f} USD
# BBOOK: {bbook_value:,.3f} USD
# CBOOK: {cbook_value:,.3f} USD
# Cent BBOOK: {cent_bbook_value:,.3f} USD

# Total balance: {df.T[0].sum():,.3f} USD
# '''.replace(',', ' '))

#     finally:
#         # Закрываем соединение с базой данных
#         connection.close()

#     return result

# # Пример вызова функции
# print(result_string('NEO', "Balance"))
