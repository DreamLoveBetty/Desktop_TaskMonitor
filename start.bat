@echo off
REM ���� ComfyUI �İ�װĿ¼
set COMFYUI_DIR="D:\Program\comfy_torch2.4\ComfyUI_windows_portable"

REM ���� Python ������·�� (python.exe)
set PYTHON_EXE="D:\Program\comfy_torch2.4\ComfyUI_windows_portable\python_embeded\python.exe"
REM ���� PythonW ������·�� (pythonw.exe)��ͨ���� python.exe ��ͬһĿ¼
echo Starting Task Monitor Widget via its own batch file...
set WIDGET_LAUNCHER_BAT="D:\Program\comfy_torch2.4\ComfyUI_windows_portable\Desktop_TaskMonitor\��������.bat"

echo Starting ComfyUI...
REM ȷ�� ComfyUI ʹ�� python.exe ��������ͨ����Ҫ����̨
start "ComfyUI" %PYTHON_EXE% ComfyUI\main.py --windows-standalone-build --disable-xformers  --front-end-version Comfy-Org/ComfyUI_frontend@latest --preview-method auto 

REM ʹ�� call ��ִ��С�������������ļ�
call %WIDGET_LAUNCHER_BAT%

echo Launch commands issued.