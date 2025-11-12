from files_for_fin_rep_dop import *
def make_answer() -> str:
    # Формирование Отчета 
    Neo_MU_absolut, Neo_MU_prozent = count_balance_Unity(Neo_MU_accaunts, Neo_MU_Key)
    Neo_KZ_absolut, Neo_KZ_prozent = count_balance_Unity(Neo_KZ_accaunts, Neo_KZ_Key)
    ARK_Capital_absolut, ARK_Capital_prozent = count_balance_Unity(ARK_Capital_accaunts, ARK_Capital_Key)

    Andery = count_profit(*get_dynamic_balance_bybit(), CONST=ANREY)
    Nitsan_dayly, Nitsan_global = get_Nitsan_profits()

    gvido_1 = count_profit(*get_binance_balance(2, 'FUTURES', 'Гвидо 1'), CONST=GVIDO_1)
    # gvido_2 = count_profit(*get_binance_balance(2, 'FUTURES', 'Гвидо 2'), CONST=GVIDO_2)
    res_summ_Anton = sum(count_balance_Unity(accs, key, True)
                for accs, key in ((Neo_MU_accaunts, Neo_MU_Key),
                                    (Neo_KZ_accaunts, Neo_KZ_Key),
                                    (ARK_Capital_accaunts, ARK_Capital_Key)))
    answer = f'''
    1. Нитсан: 
        1. Прирост отностительно прошлого дня: {Nitsan_dayly:.2f} %
        2. Прирост за все время: {Nitsan_global:.2f} %

    2. Crypto Asset Management на {gvido_1[0]}
        a. Андрей на {Andery[0]}
            1. Прирост относительно прошлого деня: {Andery[1]}
            2. Прирост за все время: {Andery[2]}
        
    3. Антон
        a. Unity Scope: Данных нет
        b. ARK Unity
            * Прирост относительно прошлого деня
                1. Абсолютное значение: {ARK_Capital_absolut:.2f} USD
                2. Процентное значение: {ARK_Capital_prozent}

        c. Exante NEO KZ
            * Прирост относительно прошлого деня
                1. Абсолютное значение: {Neo_KZ_absolut:.2f} USD
                2. Процентное значение: {Neo_KZ_prozent}

        d. Exante Exante NEO MAU
            * Прирост относительно прошлого деня
                1. Абсолютное значение: {Neo_MU_absolut:.2f} USD
                2. Процентное значение: {Neo_MU_prozent}

        e. Total PnL (Антон) на {gvido_1[0]} 23:59:59 за день:
            Total PnL: {(ARK_Capital_absolut + Neo_KZ_absolut + Neo_MU_absolut):,.2f} USD
        '''
    return answer

import requests
import time
import threading
import schedule

# Настройки бота
CHAT_ID = -1002424482482  # Ваш chat_id (может быть отрицательным для групп)
BOT_TOKEN = '7762156208:AAFY0WLe17_7wNzcdPcTTA9G5b_3VAOhU4s'
API_URL = f'https://api.telegram.org/bot{BOT_TOKEN}'


def send_message_to_telegram(message: str, chat_id: int = CHAT_ID) -> dict:
    """
    Отправляет сообщение через Telegram Bot API.

    :param message: Текст сообщения.
    :param chat_id: Идентификатор чата.
    :return: JSON-ответ API (словарь), либо пустой словарь в случае ошибки.
    """
    url = f"{API_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.HTTPError:
        print("Ошибка при отправке сообщения:", response.text)
        return {}


def send_report(chat_id: int = CHAT_ID):
    # Здесь формируйте свой отчет
    report_text = make_answer()
    send_message_to_telegram(report_text, chat_id)


def job_scheduler():
    # Запланировать выполнение функции send_report каждый день в 07:00
    schedule.every().day.at("04:00").do(send_report)
    while True:
        schedule.run_pending()
        time.sleep(30)


def answer_callback(callback_query_id: str):
    """
    Подтвердить callback_query, чтобы убрать вращалку у пользователя.
    """
    url = f"{API_URL}/answerCallbackQuery"
    requests.post(url, json={"callback_query_id": callback_query_id})


def polling():
    """
    Обычный long-polling для получения обновлений от Telegram.
    Обрабатываем команду /report и нажатие кнопки.
    """
    offset = None
    while True:
        params = {"timeout": 100, "offset": offset}
        try:
            resp = requests.get(f"{API_URL}/getUpdates", params=params)
            data = resp.json()
            for update in data.get('result', []):
                offset = update['update_id'] + 1

                # Обработка нажатия кнопки
                if 'callback_query' in update:
                    cq = update['callback_query']
                    if cq.get('data') == 'get_report':
                        chat_id = cq['message']['chat']['id']
                        send_report(chat_id)
                        answer_callback(cq['id'])

                # Обработка текстовых команд
                elif 'message' in update and 'text' in update['message']:
                    msg = update['message']
                    text = msg['text']
                    chat_id = msg['chat']['id']
                    if text == '/report':
                        # Отправляем кнопку для запроса отчета
                        keyboard = {
                            'inline_keyboard': [
                                [
                                    {'text': 'Получить отчет', 'callback_data': 'get_report'}
                                ]
                            ]
                        }
                        requests.post(
                            f"{API_URL}/sendMessage",
                            json={
                                'chat_id': chat_id,
                                'text': 'Нажмите кнопку ниже, чтобы получить отчет:',
                                'reply_markup': keyboard
                            }
                        )
        except Exception as e:
            print("Ошибка polling:", e)
            time.sleep(5)


if __name__ == '__main__':
    # Запускаем планировщик в отдельном потоке
    scheduler_thread = threading.Thread(target=job_scheduler, daemon=True)
    scheduler_thread.start()

    # Запускаем polling в основном потоке
    polling()