@echo off
echo Building Navia Dratp Digital executable...

pyinstaller ^
  --windowed ^
  --name NaviaDratpDigital ^
  --add-data "assets;assets" ^
  --add-data "data;data" ^
  main.py

echo.
echo Build complete. Check the dist\NaviaDratpDigital folder.
pause
