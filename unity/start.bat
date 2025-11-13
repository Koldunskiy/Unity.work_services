@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo Запуск всех ботов Unity Work Services...

if not exist "start.py" (
    echo ОШИБКА: start.py не найден!
    pause
    exit /b 1
)

poetry run python start.py --all

echo.
echo Все боты запущены! Нажмите любую клавишу для выхода...
pause