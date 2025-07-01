@echo off
REM Speech Transcriber Runner Script for Windows
REM This script helps you choose and run different versions of the speech transcriber

echo === Speech Transcriber ===
echo.
echo Choose a version to run:
echo 1. Standard Version (transcriber.py)
echo 2. Improved Version (transcriber_improved.py)
echo 3. Fast Version (transcriber_fast.py)
echo 4. Real-time Version (transcriber_realtime.py)
echo 5. Log Viewer (log_viewer.py)
echo 6. Exit
echo.

REM Check if virtual environment exists and activate it
if exist "venv" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo Warning: Virtual environment not found. Make sure dependencies are installed.
)

:menu
set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" (
    echo Starting Standard Version...
    python transcriber.py
    goto continue
)
if "%choice%"=="2" (
    echo Starting Improved Version...
    python transcriber_improved.py
    goto continue
)
if "%choice%"=="3" (
    echo Starting Fast Version...
    python transcriber_fast.py
    goto continue
)
if "%choice%"=="4" (
    echo Starting Real-time Version...
    python transcriber_realtime.py
    goto continue
)
if "%choice%"=="5" (
    echo Starting Log Viewer...
    python log_viewer.py
    goto continue
)
if "%choice%"=="6" (
    echo Exiting...
    exit /b 0
)

echo Invalid option. Please choose 1-6.
goto menu

:continue
echo.
pause
echo.
echo === Speech Transcriber ===
echo.
echo Choose a version to run:
echo 1. Standard Version (transcriber.py)
echo 2. Improved Version (transcriber_improved.py)
echo 3. Fast Version (transcriber_fast.py)
echo 4. Real-time Version (transcriber_realtime.py)
echo 5. Log Viewer (log_viewer.py)
echo 6. Exit
echo.
goto menu 