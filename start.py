import json
import os
import subprocess

# JSON данные
data = [
    {
        "description": "Отслеживание сделок на Binance. Передача сделок трейдеров в Unity и Backoffice.",
        "path": r"C:\work_services\Binance_Connector",
        "activate": "python main.py"
    },
    {
        "description": "Отслеживание сделок на OKX. Передача сделок трейдеров в Unity и Backoffice.",
        "path": r"C:\work_services\OKX_Connector",
        "activate": "python main.py"
    },
    {
        "description": "Отчет по торговле трейдера из эксель файла.",
        "path": r"C:\work_services\Reports_from_excel_very_important_bot",
        "activate": "call excel_report_bot\\Scripts\\activate.bat && python main.py"
    },
    {
        "description": "Парсинг телеграмм канала на торговые идеи..",
        "path": r"C:\work_services\parsing trade ides from telegram",
        "activate": "python parsing_ideas_from_TG.py"
    },
    # {
    #     "description": "Бектест торговых идей в Unity.",
    #     "path": r"C:\work_services\back_test trades ideas",
    #     "activate": "python bot_for_Unity_ideas.py"
    # },
    {
        "description": "Swap bot, отчет по проверенным сделкам Unity.",
        "path": r"C:\work_services\back_test trades ideas",
        "activate": "python main.py"
    },


]

# Функция для активации файлов
def activate_files(data):
    for item in data:
        path = item["path"]
        activate_command = item["activate"]
        
        # Формирование команды для запуска в новом окне cmd
        command = f'start cmd /K "cd /d {path} && {activate_command}"'
        
        # Запуск команды
        subprocess.Popen(command, shell=True)

# Активация всех файлов
activate_files(data)