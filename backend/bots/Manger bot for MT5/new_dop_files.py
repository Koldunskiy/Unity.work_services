import pandas as pd
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


from tabulate import tabulate
import telebot




def send_summary_to_telegram(df, df_2, company,  caption=None):
    """
    Формирует и отправляет сводку в одну строку в Telegram:
    Balance и Equity с разбивкой на ABOOK/BBOOK.
    df - balance
    df_2 - Equity
    """

    def format_number(n):
        return f"{int(n):,}".replace(",", "’") + " USD"

    # Извлекаем значения
    total_balance = format_number(df.Balance.iloc[0])
    abook_balance = format_number(df.ABOOK.iloc[0])
    bbook_balance = format_number(df.BBOOK.iloc[0])

    total_equity = format_number(df_2.Equity.iloc[0])
    abook_equity = format_number(df_2.ABOOK.iloc[0])
    bbook_equity = format_number(df_2.BBOOK.iloc[0])
    date = datetime.datetime.strftime(df.Date[0], '%d-%m-%Y')

    summary = f'''
{company}
Дата: {date}
#Балансы
Total: {total_balance} 
ABOOK: {abook_balance}
BBOOK: {bbook_balance}

#Эквити без кредита
Total: {total_equity} 
ABOOK: {abook_equity} 
BBOOK: {bbook_equity} 
'''
    if caption:
        summary = f"*{caption}*\n{summary}"

    return summary


def read_sql(path: str):
    connection = mysql.connector.connect(**CONFIG_1)
    with open(path, mode='r', encoding='utf-8')  as f:
        data = f.read()
    df = pd.read_sql_query(data, con=connection)
    connection.close()
    return df




def balance_and_E(broker: str):
    'Принимает на вход название Брокера(NEO, EKTIV) и возвращает готовую строку'
    if broker == 'NEO':
        company = 'Neo MU'
        df_balance = read_sql(r'query_new\Балансы и эквити 2 запроса нео эктив\НЕО\НЕО Балансы.txt')
        df_eq = read_sql(r'query_new\Балансы и эквити 2 запроса нео эктив\НЕО\НЕО Эквити.txt')
        return send_summary_to_telegram(df=df_balance, df_2=df_eq, company=company, caption='#Баланс и Эквити📊')
    else:
        company = 'Active Broker'
        df_balance = read_sql(r'query_new\Балансы и эквити 2 запроса нео эктив\Active\Active балансы.txt')
        df_eq = read_sql(r'query_new\Балансы и эквити 2 запроса нео эктив\Active\Active эквити.txt')
        return send_summary_to_telegram(df=df_balance, df_2=df_eq, company=company, caption='#Баланс и Эквити📊')



def PNL_get(broker: str):
    'Принимает на вход название Брокера (NEO, EKTIV) и возвращает готовую однострочную строку PNL'
    # Neo MU или Active Broker
    if broker == 'NEO':
        company = 'Neo MU'
        df_1 = read_sql(r'query_new\ПНЛ показатели нео эктив\NEO\NEO АБУК + ББУК часть без партнёров.txt')
        df_2 = read_sql(r'query_new\ПНЛ показатели нео эктив\NEO\NEO АБУК часть.txt')
        df_3 = read_sql(r'query_new\ПНЛ показатели нео эктив\NEO\NEO ББУК часть.txt')
    else:
        company = 'Active Broker'
        df_1 = read_sql(r'query_new\ПНЛ показатели нео эктив\Active\Active АБУК + ББУК часть без партнёров.txt')
        df_2 = read_sql(r'query_new\ПНЛ показатели нео эктив\Active\Active АБУК часть.txt')
        df_3 = read_sql(r'query_new\ПНЛ показатели нео эктив\Active\Active ББУК часть.txt')

    def format_number(n):
        return f"{round(n):,}".replace(",", "’") + " USD"

    # Вспомогательная функция для генерации блока
    def build_block(title, today, yesterday, curr_week, past_week, curr_month):
        return (
            f'''\n🔹 *{title}* 
Сегодня: {format_number(today)} 
Вчера: {format_number(yesterday)}
Тек. неделя: {format_number(curr_week)}
Пред. неделя: {format_number(past_week)}
Тек. месяц: {format_number(curr_month)}''')
        

    # Генерация блоков
    block_1 = build_block(
        f"ABOOK + BBOOK PL {company} (без выплат партнёров)",
        df_1['PL_kompani_Bbok_Abook_Today'].iloc[0],
        df_1['PL_kompani_Bbok_Abook_YESTERDAY'].iloc[0],
        df_1['PL_kompani_Bbok_Abook_WEEK'].iloc[0],
        df_1['PL_kompani_Bbok_Abook_past_WEEK'].iloc[0],
        df_1['PL_kompani_Bbok_Abook_MONTH'].iloc[0]
    )

    block_2 = build_block(
        f"ABOOK PL {company}",
        df_2['Today'].iloc[0],
        df_2['Yesterday'].iloc[0],
        df_2['Current_Week'].iloc[0],
        df_2['past_Week'].iloc[0],
        df_2['Current_Month'].iloc[0]
    )

    block_3 = build_block(
        f"BBOOK PL {company}",
        df_3['PL_kompani_Bbok_Today'].iloc[0],
        df_3['PL_kompani_Bbok_YESTERDAY'].iloc[0],
        df_3['PL_kompani_Bbok_WEEK'].iloc[0],
        df_3['PL_kompani_past_WEEK'].iloc[0],
        df_3['PL_kompani_Bbok_MONTH'].iloc[0]
    )

    # Сборка в одну строку (Telegram-friendly)
    caption = "*#PNL📈*"
    summary = f"{caption}{block_1}\n{block_2}\n{block_3}"

    # Усечём, если больше 4000 символов
    if len(summary) > 4000:
        summary = summary[:3990] + "\n..."

    return summary


