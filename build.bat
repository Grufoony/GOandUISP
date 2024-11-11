@echo off
set /p buildType="Enter the build type (e.g., BSL): "

pip install .

if /I "%buildType%"=="BSL" (
    python -m PyInstaller --onefile .\races\bsl\bsl.py
) else if /I "%buildType%"=="bsl" (
    python -m PyInstaller --onefile .\races\bsl\bsl.py
) 
if /I "%buildType%"=="sonopronto" (
    python -m PyInstaller --onefile .\races\sono_pronto\sono_pronto.py
) else (
    echo Unknown build type: %buildType%
)
pause