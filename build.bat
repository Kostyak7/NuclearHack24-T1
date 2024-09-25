@echo on

IF NOT "%1"=="" (
	goto %~1 
) ELSE (
	call init.bat check
	goto run
)

:update
call git restore .
call git pull
goto init

:init
call init.bat init
goto run

:run
cd frontend
call npm run build
cd ..
call venv\Scripts\activate
cls
start http://127.0.0.1:8000
call python manage.py runserver

:end