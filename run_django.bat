@echo off
cd /d "%~dp0"
call venv\Scripts\activate
echo Website: http://127.0.0.1:8000/   Admin: http://127.0.0.1:8000/admin/
python manage.py runserver
