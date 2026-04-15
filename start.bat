@echo off
chcp 65001 >nul
echo ========================================
echo    语音克隆系统 - Windows 启动脚本
echo ========================================
echo.

REM 检查 Docker 是否运行
docker info >nul 2>&1
if errorlevel 1 (
    echo [错误] Docker 未运行，请先启动 Docker Desktop
    echo.
    pause
    exit /b 1
)

echo [信息] Docker 已就绪
echo [信息] 正在启动服务...
echo.

docker compose up --build

pause
