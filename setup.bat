@echo off
REM ===== Meerut Hospital - one-time setup (Windows) =====
cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
    echo Python nahi mila. python.org se Python 3.11+ install karo.
    pause
    exit /b 1
)

if not exist venv (
    echo Virtual environment bana raha hoon...
    python -m venv venv
)

call venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

python manage.py makemigrations hospital
python manage.py migrate
python manage.py seed_doctors

echo.
echo ===== Ab admin account banao (username, email, password) =====
python manage.py createsuperuser

echo.
echo Setup complete! Ab run_django.bat aur run_api.bat chalao.
pause
