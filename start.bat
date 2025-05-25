@echo off
REM 设置 ComfyUI 的安装目录
set COMFYUI_DIR="D:\Program\comfy_torch2.4\ComfyUI_windows_portable"

REM 设置 Python 解释器路径 (python.exe)
set PYTHON_EXE="D:\Program\comfy_torch2.4\ComfyUI_windows_portable\python_embeded\python.exe"
REM 设置 PythonW 解释器路径 (pythonw.exe)，通常与 python.exe 在同一目录
echo Starting Task Monitor Widget via its own batch file...
set WIDGET_LAUNCHER_BAT="D:\Program\comfy_torch2.4\ComfyUI_windows_portable\Desktop_TaskMonitor\启动程序.bat"

echo Starting ComfyUI...
REM 确保 ComfyUI 使用 python.exe 启动，它通常需要控制台
start "ComfyUI" %PYTHON_EXE% ComfyUI\main.py --windows-standalone-build --disable-xformers  --front-end-version Comfy-Org/ComfyUI_frontend@latest --preview-method auto 

REM 使用 call 来执行小部件的批处理文件
call %WIDGET_LAUNCHER_BAT%

echo Launch commands issued.