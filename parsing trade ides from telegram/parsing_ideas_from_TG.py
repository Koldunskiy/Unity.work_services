from datetime import datetime, timedelta
import requests
import json
import pandas as pd
BOT_TOKEN = '6904289392:AAHIyb4BfEESn7RcZWJ7qOSvuVNWodSkWtU'
CHAT_ID = '-1002245059823'
"'620211681' -  чат id бота, куда приходят мне ошибки"

import telebot

TOKEN = BOT_TOKEN
bot = telebot.TeleBot(TOKEN)


import logging

logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
                    filename='telegramm_ideas.log', 
                    filemode='w')

logger = logging.getLogger(__name__)



def make_dict(message:str) -> dict:
  lines = [line.strip() for line in message.strip().split('\n') if line.strip()]
  data_dict = {}
  for line in lines:
      if ':' in line:
          key, value = line.split(':', 1)
          data_dict[key.strip()] = value.strip()
  data_dict['headlinear'] = data_dict['Instrument'] + ' ' + data_dict['Side'] +  ' Signal'
  data_dict['Description'] = '\n' + data_dict['Description']
  return data_dict


def export_idea(data_dict) -> requests.post:
  key_data = pd.read_csv('IDes for Unity Instruments.csv')

  def make_correct_time(time:str, delta:int=0) -> str:
    date_obj = datetime.strptime(time, '%d.%m.%Y %H:%M')
    date_obj += timedelta(hours=delta)
    formatted_date = date_obj.strftime('%Y-%m-%dT%H:%M:%SZ')
    return formatted_date

  target = {
    "instrumentIds": [int(i) for i in key_data.loc[key_data['ticker'] == data_dict.get('Instrument', None)]['id'].iloc[0].split(',')],
    "openOrderType": "LIMIT",
    "side": (data_dict['Side']).upper(),
    "price": float(data_dict['Entry Level'].replace(',', '.')),
    "stopLoss": float(data_dict['Stop Loss'].replace(',', '.')),
    "takeProfit": float(data_dict['Take Profit'].replace(',', '.')),
    "confidence": 0,
    "expirationTime": make_correct_time(time=data_dict['Date/Time'], delta=int(data_dict['Relevance'].split()[0])),
    "localeDescriptions": [
      {
        "locale": 'EN',
        "target": data_dict['headlinear'],
        "background": data_dict['Description']
      }
    ],
    "publishTime": make_correct_time(time=data_dict['Date/Time']),
    "state": "LIVE_TRADE",
    "provider": "UNITY",
    "rate": 0,
    "externalId": "string",
    "sorce": (data_dict['Source']),
    "priority": 0
    }
  payload =  json.dumps(target, indent=4, ensure_ascii=False)

  url = 'https://rest.unity.finance/api/v1/createTradeIdea'
  token = 'c3f28d5b-9694-4307-b30f-6f800ee13506'
  headers = {
        "accept": "application/json",
        "auth-token": token
    }
  response = requests.post(url, headers=headers, data=(payload))
    
  if response.status_code != 200:
      bot.send_message('6904289392', f'Failed to create trade idea. Status code: {response.status_code}, Response: {response.text}. Ошибка в отправлении сообщения по API Unity')
      logger.error(f'Failed to create trade idea. Status code: {response.status_code}, Response: {response.text}. Ошибка в отправлении сообщения по API Unity')



@bot.channel_post_handler(content_types=['text'])
def echo_to_channel(message):
    data_dict = (make_dict(message.text))
    try:
        export_idea(data_dict)
        print('Успех!')
    except Exception as e:
       bot.send_message('620211681', f'{e}, ошибка')
       logger.error(e)
      #  print(target)

print('Бот для парсиена идей из ТГ запустился')
while True:
   try:
      bot.polling()

   except Exception as e:
      logging.error(e)
      print(e)