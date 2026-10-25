@echo off
cd /d "%~dp0"
call venv\Scripts\activate
echo API docs: http://127.0.0.1:8001/docs
python -m uvicorn fastapi_app:app --reload --port 8001
