@echo off
title Python Analytics Dashboard
echo ==========================================
echo      Python Analytics Dashboard
echo ==========================================
echo.
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)
call venv\Scripts\activate
echo Installing/updating dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
echo.
echo Starting Streamlit...
streamlit run app.py
pause
