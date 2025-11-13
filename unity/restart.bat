@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo Перезапуск ботов...
poetry run python start.py --stop
timeout /t 2 >nul
poetry run python start.py --all
echo.
echo Боты перезапущены!
pause