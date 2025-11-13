"""
start.py — менеджер запуска и остановки ботов Unity Work Services.

Функционал:
- --all      : запуск всех ботов в фоне
- --stop     : остановка всех текущих ботов
- --list     : вывод списка доступных ботов
- --index N,M: запуск выбранных ботов по индексам

Боты запускаются через `poetry run python` в отдельных процессах.
PID сохраняются в `running_pids.txt` для точной остановки.
"""

import argparse
import concurrent.futures
import logging
import os
import subprocess
import sys
from pathlib import Path

import psutil

# --------------------------------------------------------------------------- #
# Логирование
# --------------------------------------------------------------------------- #
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("start.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)

# Скрытие консольных окон на Windows
CREATE_NO_WINDOW = 0x08000000 if sys.platform == "win32" else 0

# --------------------------------------------------------------------------- #
# Определение корня проекта
# --------------------------------------------------------------------------- #
ROOT_DIR = Path(__file__).parent
while not (ROOT_DIR / "backend").exists() and ROOT_DIR.parent != ROOT_DIR:
    ROOT_DIR = ROOT_DIR.parent

if not (ROOT_DIR / "backend").exists():
    raise RuntimeError("Не могу найти папку backend! Проверь структуру проекта.")

# --------------------------------------------------------------------------- #
# Описание ботов
# --------------------------------------------------------------------------- #
DATA = [
    {
        "description": "Отслеживание сделок на Binance. Передача сделок трейдеров в Unity и Backoffice.",
        "path": os.path.join(ROOT_DIR, "backend", "connectors", "Binance_Connector"),
        "activate": "python main.py",
    },
    {
        "description": "Отслеживание сделок на OKX. Передача сделок трейдеров в Unity и Backoffice.",
        "path": os.path.join(ROOT_DIR, "backend", "connectors", "OKX_Connector"),
        "activate": "python main.py",
    },
    {
        "description": "Отчет по торговле трейдера из эксель файла.",
        "path": os.path.join(ROOT_DIR, "backend", "bots", "Reports_from_excel_very_important_bot"),
        "activate": "python main.py",
    },
    {
        "description": "Парсинг телеграмм канала на торговые идеи.",
        "path": os.path.join(ROOT_DIR, "backend", "bots", "parsing trade ides from telegram"),
        "activate": "python parsing_ideas_from_TG.py",
    },
    {
        "description": "Swap bot, отчет по проверенным сделкам Unity.",
        "path": os.path.join(ROOT_DIR, "backend", "bots", "back_test trades ideas"),
        "activate": "python main.py",
    },
    # {
    #     "description": "Бектест торговых идей в Unity.",
    #     "path": os.path.join(ROOT_DIR, "backend", "bots", "back_test trades ideas"),
    #     "activate": "python bot_for_Unity_ideas.py"
    # },
]

PID_FILE = ROOT_DIR / "unity" / "running_pids.txt"


# --------------------------------------------------------------------------- #
def run_script(item: dict) -> None:
    """
    Запускает один бот в отдельном процессе через `poetry run python`.

    PID записывается в `running_pids.txt` для последующей остановки.
    """
    path = item["path"]
    activate = item["activate"]
    description = item["description"]

    if not os.path.exists(path):
        logger.error(f"Путь не найден: {path} ({description})")
        return

    try:
        cmd = ["poetry", "run", "python"] + activate.split()[1:]

        env = os.environ.copy()
        python_path = env.get("PYTHONPATH", "")
        python_path = str(ROOT_DIR) + os.pathsep + python_path
        env["PYTHONPATH"] = python_path

        process = subprocess.Popen(
            cmd,
            env=env,
            cwd=path,
            creationflags=CREATE_NO_WINDOW,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        logger.info(f"Запущен: {description} (PID: {process.pid})")

        # Сохраняем PID
        with open(PID_FILE, "a", encoding="utf-8") as f:
            f.write(f"{process.pid}|{description}|{path}\n")

    except Exception as e:
        logger.error(f"Ошибка запуска {description}: {e}")


# --------------------------------------------------------------------------- #
def get_bot_pids() -> list[int]:
    """
    Возвращает список PID текущих ботов из файла `running_pids.txt`.

    Если файл отсутствует — возвращает пустой список.
    """
    if not PID_FILE.exists():
        return []

    pids = []
    with open(PID_FILE, "r", encoding="utf-8") as f:
        for line in f:
            pid_str = line.strip().split("|", 1)[0]
            try:
                pids.append(int(pid_str))
            except ValueError:
                continue
    return pids


# --------------------------------------------------------------------------- #
def stop_all_bots() -> None:
    """
    Останавливает все боты, PID которых записаны в `running_pids.txt`.

    Процессы сначала получают SIGTERM, затем (при необходимости) SIGKILL.
    После завершения файл PID удаляется.
    """
    pids = get_bot_pids()
    if not pids:
        logger.info("Нет запущенных ботов для остановки.")
        return

    logger.info(f"Останавливаю {len(pids)} ботов (PIDs: {pids[:10]}{'...' if len(pids) > 10 else ''})...")

    # Мягкая остановка
    for pid in pids:
        try:
            proc = psutil.Process(pid)
            if proc.is_running():
                proc.terminate()
                logger.info(f"Отправлен сигнал остановки PID {pid}")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    # Ожидание завершения
    try:
        gone, alive = psutil.wait_procs(
            [psutil.Process(p) for p in pids if psutil.pid_exists(p)],
            timeout=5,
        )
    except Exception as e:
        logger.warning(f"Ошибка при ожидании процессов: {e}")
        alive = []

    # Принудительное завершение
    for p in alive:
        try:
            p.kill()
            logger.warning(f"Принудительно убит PID {p.pid}")
        except Exception:
            pass

    # Очистка файла
    if PID_FILE.exists():
        PID_FILE.unlink()
    logger.info("Все боты остановлены. Файл PID удалён.")


# --------------------------------------------------------------------------- #
def main() -> None:
    """Точка входа — парсинг аргументов и выполнение действий."""
    parser = argparse.ArgumentParser(
        description="Менеджер запуска/остановки ботов Unity Work Services"
    )
    parser.add_argument("--all", action="store_true", help="Запустить все боты")
    parser.add_argument("--stop", action="store_true", help="Остановить все запущенные боты")
    parser.add_argument("--index", type=str, help="Запустить по индексам (0,2)")
    parser.add_argument("--list", action="store_true", help="Показать список ботов")

    args = parser.parse_args()

    # Остановка
    if args.stop:
        stop_all_bots()
        return

    # Список
    if args.list:
        for i, item in enumerate(DATA):
            print(f"{i}: {item['description']} (путь: {item['path']})")
        return

    # Подготовка задач
    tasks = []
    if args.all:
        tasks = DATA
    elif args.index:
        indices = [int(idx.strip()) for idx in args.index.split(",") if idx.strip().isdigit()]
        tasks = [DATA[i] for i in indices if i < len(DATA)]
    else:
        parser.print_help()
        return

    if not tasks:
        logger.warning("Нет задач для запуска.")
        return

    # Очистка старого файла PID при новом запуске
    if PID_FILE.exists():
        PID_FILE.unlink()
        logger.info("Очищен старый файл running_pids.txt")

    # Параллельный запуск
    with concurrent.futures.ProcessPoolExecutor(max_workers=len(tasks)) as executor:
        futures = [executor.submit(run_script, item) for item in tasks]
        concurrent.futures.wait(futures)

    logger.info("Все скрипты запущены.")


# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    main()