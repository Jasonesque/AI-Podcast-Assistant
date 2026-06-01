@echo off
chcp 65001 >nul
color 0A
title 播客 AI 助手

echo ===================================================
echo               播客 AI 助手 (本地快速启动)
echo ===================================================
echo.
set /p url="请粘贴播客/视频链接 (鼠标右键点击即可粘贴) 并按回车: "

if "%url%"=="" (
    echo.
    echo [错误] 链接不能为空！
    pause
    exit /b
)

echo.
echo 正在启动 AI 引擎处理该链接，请稍候...
echo.
call venv\Scripts\python.exe main.py "%url%"

echo.
echo ===================================================
echo 处理完毕！你可以去 Obsidian 知识库查看生成的笔记了。
echo 按任意键退出...
pause >nul
