@echo on

:check
IF not EXIST "venv" (
	goto init
)
goto end

:init
python -m venv venv
call venv\Scripts\activate
call pip install -r requirements.txt
call deactivate
cd frontend
call npm i vue-cli-service
call npm audit dix
cd ..

setlocal
set "DESTINATION=/algorithms/my_models/" 
set "SEARCH_TOC_MODEL_FILE_ID=1bwjw0-bqXUv6A0eBX9QSnbrSFAciur82"  
set "CREATE_TOC_MODEL_FILE_ID=13WCecdc7vrdXoh3HD50fvOqKySMyw5cb"  

curl -L -o "%DESTINATION%" "https://drive.google.com/uc?export=download&id=%SEARCH_TOC_MODEL_FILE_ID%"
curl -L -o "%DESTINATION%" "https://drive.google.com/uc?export=download&id=%CREATE_TOC_MODEL_FILE_ID%"
endlocal

:end