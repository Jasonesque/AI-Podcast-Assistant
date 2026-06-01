@echo off
cd /d "%~dp0"
chcp 65001 >nul
color 0B
title 飞书服务端与穿透隧道

echo ===================================================
echo               播客 AI 助手 (飞书后台服务)
echo ===================================================
echo.
echo [1/2] 正在启动本地 AI 处理引擎与监听服务...
:: 弹出一个新窗口运行 FastAPI 服务端
start "飞书本地 AI 服务器" cmd /k "venv\Scripts\python.exe server.py"

echo [2/2] 正在启动 Cloudflare 全球穿透隧道...
echo.
echo ***************************************************************
echo 请注意看下方的日志！
echo 找到里面类似 https://xxx-yyy-zzz.trycloudflare.com 的网址。
echo 这个就是你的专属机器人外网地址！
echo ***************************************************************
echo.
:: 启动隧道，映射到本地 8000 端口
cloudflared tunnel --url http://127.0.0.1:8000

pause
