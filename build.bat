@echo off
set /p buildType="Enter the build type (bsl - sonopronto - youngchallenge): "

pip install .

if /I "%buildType%"=="bsl" (
    python -m PyInstaller --onefile .\races\bsl\bsl.py
    python -m PyInstaller --onefile .\races\bsl\ranker.py
) else if /I "%buildType%"=="sonopronto" (
    python -m PyInstaller --onefile .\races\sono_pronto\sono_pronto.py
) else if /I "%buildType%"=="youngchallenge" (
    python -m PyInstaller --onefile .\races\young_challenge\young_challenge.py
) else (
    echo Unknown build type: %buildType%
)
pause