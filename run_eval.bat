@echo off
REM run_eval.bat
REM This script clears previous ADK evaluation history and runs a fresh evaluation.

echo Cleaning up previous evaluation history...

REM Define paths
set "HISTORY_PATH=medical_agent\.adk\eval_history"
set "CACHE_PATH=.adk_eval_cache"

REM Clear history
if exist "%HISTORY_PATH%" (
    del /q /s "%HISTORY_PATH%\*" >nul 2>&1
    echo ^| Cleared eval history.
)

REM Clear cache
if exist "%CACHE_PATH%" (
    rmdir /s /q "%CACHE_PATH%" >nul 2>&1
    echo ^| Cleared eval cache.
)

echo Starting ADK Evaluation...

REM Run the evaluation
adk eval medical_agent eval/test.json --config_file_path=eval/test_config.json

echo Evaluation Complete!
