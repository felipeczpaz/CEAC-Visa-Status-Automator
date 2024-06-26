@echo off

REM Install Python if not already installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing Python...
    REM Download Python installer (adjust URL as needed)
    bitsadmin /transfer "PythonInstaller" https://www.python.org/ftp/python/3.9.12/python-3.9.12-amd64.exe %TEMP%\python-3.9.12-amd64.exe
    REM Install Python silently
    %TEMP%\python-3.9.12-amd64.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    REM Check installation
    python --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo Error: Python installation failed.
        exit /b 1
    )
    echo Python installation successful.
) else (
    echo Python is already installed.
)

REM Install required Python packages using pip
echo Installing required Python packages...
python -m pip install --upgrade pip setuptools
python -m pip install PyPDF2 selenium

REM Check installation of required packages
pip show PyPDF2 >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: PyPDF2 installation failed.
    exit /b 1
)
pip show selenium >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: selenium installation failed.
    exit /b 1
)
echo Required Python packages installation successful.

REM Optional: Pause at the end (remove if running from a batch file)
pause
