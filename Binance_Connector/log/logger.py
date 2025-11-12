import os
import logging
from logging.handlers import RotatingFileHandler
from typing import Optional

# Папка для логов — тот же каталог, где находится этот модуль (log/)
LOG_DIR = os.path.dirname(os.path.abspath(__file__))
os.makedirs(LOG_DIR, exist_ok=True)

def get_logger(name_or_path: Optional[str]) -> logging.Logger:
    """
    Возвращает настроенный логгер (только файловый хендлер).
    - name_or_path может быть __file__ или именем модуля; имя логгера будет совпадать с названием файла (без расширения).
    - Логи пишутся только в файл: log/<name>.log (консольный вывод отключён).
    - Файл лога ограничен 20 КБ, при достижении лимита очищается и начинается заново.
    """
    if not name_or_path:
        name = "root"
    else:
        name = os.path.splitext(os.path.basename(name_or_path))[0]

    logger = logging.getLogger(name)
    # Если уже настроен — вернуть (чтобы не дублировать хендлеры при повторном импорте)
    if getattr(logger, "_configured", False):
        return logger

    logger.setLevel(logging.INFO)
    # Формат времени и сообщения — на русском читаемом виде
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")

    # Файловый хендлер с ограничением размера (20 КБ) и очисткой при достижении лимита
    file_path = os.path.join(LOG_DIR, f"{name}.log")
    
    # Создаем RotatingFileHandler с максимальным размером 20 КБ и 1 резервным файлом
    # При достижении лимита файл будет переименован в .log.1, а текущий очищен
    fh = RotatingFileHandler(
        file_path, 
        maxBytes=10 * 1024 * 1024,  # 20 КБ
        backupCount=1,       # 1 резервный файл
        encoding="utf-8"
    )
    fh.setFormatter(formatter)
    fh.setLevel(logging.INFO)
    logger.addHandler(fh)

    # Убираем консольный хендлер — логи не показываем в консоли по запросу пользователя
    logger.propagate = False
    logger._configured = True
    
    return logger