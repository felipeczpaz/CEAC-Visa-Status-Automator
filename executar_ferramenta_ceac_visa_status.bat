@echo off

rem Define the directory where you want to store the Python script
set SCRIPT_DIR=C:\Dev
rem Define the URL of the Python script on GitHub
set SCRIPT_URL=https://raw.githubusercontent.com/felipeczpaz/CEAC-Visa-Status-Automator/main/ceac_visa_status_automator.py
rem Define the filename of the Python script
set SCRIPT_NAME=ceac_visa_status_automator.py
rem Define the full path to the Python script
set SCRIPT_PATH=%SCRIPT_DIR%\%SCRIPT_NAME%

rem Check if the script already exists
if exist "%SCRIPT_PATH%" (
    rem Check if there's a newer version on GitHub
    curl -s -o "%SCRIPT_PATH%.new" -z "%SCRIPT_PATH%" "%SCRIPT_URL%"
    rem Compare the downloaded file with the existing one
    fc /b "%SCRIPT_PATH%" "%SCRIPT_PATH%.new" > nul
    if errorlevel 1 (
        echo Updating the script...
        move /y "%SCRIPT_PATH%.new" "%SCRIPT_PATH%"
    ) else (
        del "%SCRIPT_PATH%.new" > nul
        echo Script is up to date.
    )
) else (
    rem If the script doesn't exist, download it
    echo Script not found. Downloading...
    curl -o "%SCRIPT_PATH%" "%SCRIPT_URL%"
)

rem Check if the script exists before attempting to run it
if exist "%SCRIPT_PATH%" (
    rem Execute the Python script
    python "%SCRIPT_PATH%"
) else (
    echo Failed to download the script from GitHub.
    pause
)
