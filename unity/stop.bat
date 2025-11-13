@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo Остановка всех ботов...

if not exist "start.py" (
    echo ОШИБКА: start.py не найден!
    pause
    exit /b 1
)

poetry run python start.py --stop

echo.
echo Все боты остановлены!
pause