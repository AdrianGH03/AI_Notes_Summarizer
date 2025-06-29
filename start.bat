@echo off
echo Starting AI Notes Summarizer with Docker...
echo.
echo This will start:
echo - Backend API (http://localhost:8000)
echo - Frontend UI (http://localhost:3000)
echo - PostgreSQL Database
echo.
echo Press Ctrl+C to stop all services
echo.

docker compose up --build
