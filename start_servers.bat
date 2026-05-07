@echo off
echo Starting Hospital Specialist A2A Servers using uvicorn...

start /B uvicorn neurologist.server:app --port 8001 > nul 2>&1
start /B uvicorn cardiologist.server:app --port 8002 > nul 2>&1
start /B uvicorn pulmonologist.server:app --port 8003 > nul 2>&1
start /B uvicorn nephrologist.server:app --port 8004 > nul 2>&1
start /B uvicorn gastrologist.server:app --port 8005 > nul 2>&1

echo All specialist A2A servers started in the background.
echo You can now run 'streamlit run streamlit_app.py' to test the system.
