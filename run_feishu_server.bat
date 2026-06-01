@echo off
cd /d "%~dp0"
chcp 65001 >nul
color 0B
title Podcast AI Server

echo ===================================================
echo         Podcast AI Assistant (Feishu WebSocket)
echo ===================================================
echo.
echo Starting local WebSocket server...
echo (Connecting directly to Feishu, no Ngrok required)
echo.
call venv\Scripts\python.exe ws_server.py

pause
