@echo off

rem TaskVoyage 项目启动脚本（批处理版）
rem 功能：启动后端服务和Vue 3前端服务，并自动打开浏览器访问项目主页面

setlocal

echo =========================================
echo         TaskVoyage 启动脚本          
echo =========================================
echo.

rem 检查Python是否安装
echo 检查Python环境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误：未检测到Python环境，请先安装Python
    pause
    exit /b 1
)
echo Python环境正常
echo.

rem 检查项目目录
echo 检查项目目录...
if not exist "..\manage.py" (
    echo 错误：未找到manage.py文件，请确保在项目根目录的"启动"文件夹中运行此脚本
    pause
    exit /b 1
)
echo 项目目录正常
echo.

rem 启动后端服务
echo 启动后端服务...
start "TaskVoyage 后端服务" cmd /k "cd .. && python manage.py runserver"
echo 后端服务启动中...
echo.

rem 启动前端Vue 3服务
echo 启动前端Vue 3服务...
start "TaskVoyage 前端服务" cmd /k "cd ..\frontend-vue && npm run dev"
echo 前端Vue 3服务启动中...
echo.

rem 等待服务启动
echo 等待服务启动...
for /L %%i in (1,1,15) do (
    timeout /t 2 >nul
    curl -s http://localhost:8000 >nul 2>&1
    if %errorlevel% equ 0 (
        echo 后端服务启动成功！
        goto backend_started
    )
    echo 后端服务启动中... (%%i/15)
)

echo 警告：后端服务启动超时，可能启动失败
goto open_browser

:backend_started

:open_browser
rem 打开浏览器访问前端页面
echo 正在打开浏览器...
start http://localhost:3000
echo 浏览器已打开，正在访问Vue 3前端应用
echo.

echo =========================================
echo       TaskVoyage 启动完成！        
echo =========================================
echo 后端服务地址: http://localhost:8000
echo 前端访问地址: http://localhost:3000
echo.
echo 按任意键退出...
pause >nul

endlocal