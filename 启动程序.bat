@echo off

cd /d "%~dp0"

set PYTHONW_EXE="D:\Program\comfy_torch2.4\ComfyUI_windows_portable\python_embeded\pythonw.exe"

set WIDGET_SCRIPT_PYW="comfyui_pet_monitor.pyw"

echo ========================================
echo     ComfyUI Pet Monitor Launcher (Debug Mode)
echo ========================================
echo.
echo Current Directory (should be Desktop_TaskMonitor): %cd%
echo Python Interpreter: %PYTHONW_EXE%
echo Script to Launch: %WIDGET_SCRIPT_PYW%
echo.
echo Full command to be executed by 'start':
start "MyPetWidget" %PYTHONW_EXE% %WIDGET_SCRIPT_PYW%
echo.
