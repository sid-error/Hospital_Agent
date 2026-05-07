# start_servers.ps1
Write-Host "Starting Hospital Specialist A2A Servers using uvicorn..." -ForegroundColor Cyan

# Start each one in a new hidden or minimized window
Start-Process -NoNewWindow -FilePath "uvicorn" -ArgumentList "neurologist.server:app", "--port", "8001"
Start-Process -NoNewWindow -FilePath "uvicorn" -ArgumentList "cardiologist.server:app", "--port", "8002"
Start-Process -NoNewWindow -FilePath "uvicorn" -ArgumentList "pulmonologist.server:app", "--port", "8003"
Start-Process -NoNewWindow -FilePath "uvicorn" -ArgumentList "nephrologist.server:app", "--port", "8004"
Start-Process -NoNewWindow -FilePath "uvicorn" -ArgumentList "gastrologist.server:app", "--port", "8005"

Write-Host "All specialist A2A servers started in the background." -ForegroundColor Green
Write-Host "You can now run 'streamlit run streamlit_app.py' to test the system." -ForegroundColor Yellow
