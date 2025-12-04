@echo off
REM Job Scrapper - Streamlit Launcher
REM Auto-selects available port or kills existing instance

echo ========================================
echo    Job Scrapper - Starting...
echo ========================================

REM Activate virtual environment
call venv\Scripts\activate

REM Check if port 8501 is in use
netstat -ano | findstr :8501 | findstr LISTENING >nul
if %errorlevel%==0 (
    echo.
    echo Port 8501 is in use. Choose an option:
    echo [1] Kill existing Streamlit and restart on 8501
    echo [2] Start on different port (8502)
    echo [3] Cancel
    echo.
    set /p choice="Enter choice (1/2/3): "

    if "%choice%"=="1" (
        echo Killing existing processes on port 8501...
        for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8501 ^| findstr LISTENING') do (
            taskkill /F /PID %%a 2>nul
        )
        timeout /t 2 >nul
        echo Starting Streamlit on port 8501...
        streamlit run streamlit_app.py
    ) else if "%choice%"=="2" (
        echo Starting Streamlit on port 8502...
        streamlit run streamlit_app.py --server.port 8502
    ) else (
        echo Cancelled.
        exit /b
    )
) else (
    echo Starting Streamlit on port 8501...
    streamlit run streamlit_app.py
)
