@echo off
cd /d D:\agentic-quiz-system

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Starting FastAPI server...
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000