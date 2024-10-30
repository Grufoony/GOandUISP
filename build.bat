@echo off
set /p buildType="Enter the build type (e.g., BSL): "

if /I "%buildType%"=="BSL" (
    python -m PyInstaller --onefile .\races\bsl\bsl.py
) else if /I "%buildType%"=="bsl" (
    python -m PyInstaller --onefile .\races\bsl\bsl.py
) else (
    echo Unknown build type: %buildType%
)
pause