import logging

# Настройка логирования: все логи будут записываться в файл bot.log
logging.basicConfig(
    level=logging.INFO,
    filename="bot.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s"
)



import logging
import os
import sys
import asyncio
import pandas as pd
import quantstats as qs
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile
import matplotlib
matplotlib.use("Agg")

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    filename="bot.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Устанавливаем политику цикла событий для Windows
if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

class FinanceBot:
    def __init__(self, token: str):
        self.bot = Bot(token=token)
        self.dp = Dispatcher()
        self.download_folder = "downloads"
        self.processed_folder = "processed"
        os.makedirs(self.download_folder, exist_ok=True)
        os.makedirs(self.processed_folder, exist_ok=True)
        self.register_handlers()

    def register_handlers(self):
        @self.dp.message(CommandStart())
        async def start_handler(message: types.Message):
            text = (
                "Добро пожаловать!\n"
                "Отправьте Excel файл с данными о динамике баланса торгового счета.\n"
                "Файл должен содержать 2 столбца: дату и баланс."
            )
            await message.answer(text)

        @self.dp.message(lambda message: message.document is not None)
        async def file_handler(message: types.Message):
            try:
                file_info = await self.bot.get_file(message.document.file_id)
                downloaded_file = await self.bot.download_file(file_info.file_path)
                file_path = os.path.join(self.download_folder, message.document.file_name)
                with open(file_path, "wb") as f:
                    f.write(downloaded_file.getvalue())
                await message.reply("Файл получен, обрабатывается...")

                # Обработка файла в отдельном потоке
                processed_file_path = await asyncio.to_thread(self.process_file, file_path)

                if processed_file_path and os.path.exists(processed_file_path):
                    await message.answer_document(FSInputFile(processed_file_path))
                    os.remove(file_path)
                    os.remove(processed_file_path)
                else:
                    await message.reply("Ошибка: обработанный файл не найден.")
            except Exception as e:
                logging.exception(f"Ошибка при обработке файла: {e}")
                await message.reply(f"Ошибка: {str(e)}")

    def process_file(self, file_path: str) -> str:
        processed_file_path = os.path.join(self.processed_folder, "quantstats_report.html")
        try:
            df = pd.read_excel(file_path)
            date_col, balance_col = df.columns

            df[date_col] = pd.to_datetime(df[date_col])
            df.set_index(date_col, inplace=True)

            def count_report():
                for round_number in range(1, 8):
                    try:
                        df["Доходность"] = df[balance_col].pct_change(round_number)
                        returns = df["Доходность"].dropna()
                        qs.reports.html(returns, output=processed_file_path)
                        return processed_file_path
                    except Exception as e:
                        print(f"Попытка с округлением до {round_number} знаков не удалась: {str(e)}")
                        continue
                raise Exception("Не удалось создать отчёт с любым округлением (1-7 знаков)")

            return count_report()

        except Exception as e:
            raise Exception(f"Ошибка обработки файла: {str(e)}")

    async def run(self):
        print("Бот Finance запущен")
        try:
            await self.dp.start_polling(self.bot)
        finally:
            await self.bot.session.close()  # корректно закрываем сессию

if __name__ == "__main__":
    TOKEN = "7713078666:AAGj2JWwiVgw5mPFxqP20F05L_nntr4BmVE"
    finance_bot = FinanceBot(token=TOKEN)
    try:
        asyncio.run(finance_bot.run())  # корректный запуск асинхронного бота
    except Exception as e:
        logging.exception(f"Ошибка при запуске бота: {e}")




