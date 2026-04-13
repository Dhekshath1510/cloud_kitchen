@echo off
REM Use localhost/default config or assign inline
set PORT=8000
echo Starting Uvicorn API on Port %PORT%
uvicorn app.main:app --host 0.0.0.0 --port %PORT% --reload
