@echo off
cd /d "%~dp0"
chcp 65001 >nul
color 0B
title 飞书服务端 (长连接模式)

echo ===================================================
echo               播客 AI 助手 (飞书长连接后台服务)
echo ===================================================
echo.
echo 🚀 正在启动本地 WebSocket 服务端...
echo 🔗 这种模式不需要任何内网穿透（无需 Ngrok / Cloudflare）！
echo.
:: 启动 WebSocket 隧道服务器
call venv\Scripts\python.exe ws_server.py

pause
