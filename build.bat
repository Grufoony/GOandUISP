@echo off

pip install .
python -m PyInstaller --noconsole --onefile .\app\app.py

pause