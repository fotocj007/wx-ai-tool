@echo off
chcp 65001 >nul
echo 启动VX Tool - 微信公众号热点文章AI生成与发布系统
echo ========================================================

:: 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到Python，请先安装Python 3.7+
    pause
    exit /b 1
)

:: 切换到脚本所在目录
cd /d "%~dp0"

:: 检查虚拟环境
if exist "venv\Scripts\activate.bat" (
    echo 激活虚拟环境...
    call venv\Scripts\activate.bat
)

:: 安装依赖（如果需要）
if not exist "requirements_installed.flag" (
    echo 首次运行，安装依赖包...
    pip install -r requirements.txt
    if %errorlevel% equ 0 (
        echo. > requirements_installed.flag
        echo 依赖安装完成
    ) else (
        echo 依赖安装失败，请手动运行: pip install -r requirements.txt
        pause
        exit /b 1
    )
)

:: 启动应用
echo 启动应用...
python run.py

if %errorlevel% neq 0 (
    echo 应用启动失败
    pause
)