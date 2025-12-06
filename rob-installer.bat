@echo off
setlocal
set "NEW_PATH=C:\rob"

echo Downloading rob
curl -L -o rob.bat https://raw.githubusercontent.com/HollowTechnology/rob/refs/heads/main/rob.bat
curl -L -o rob.py  https://raw.githubusercontent.com/HollowTechnology/rob/refs/heads/main/rob.py

echo Creating C:\rob
mkdir C:\rob 2>nul

echo Copying files
robocopy . C:\rob rob.bat rob.py /R:1 /W:1 >nul

echo Cleaning up files
del rob.bat
del rob.py

echo Adding rob to Path

for /f "tokens=2*" %%A in ('reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path') do set "OLD_PATH=%%B"


echo %OLD_PATH% | find /i "%NEW_PATH%" >nul
if not errorlevel 1 (
    echo Rob already in path
    pause
    exit /b
)

setx Path "%OLD_PATH%;%NEW_PATH%" /M

echo Done, restart CMD/Powershell windows to use.
pause
