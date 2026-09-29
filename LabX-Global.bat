@echo off
REM Get the directory where this batch file is located
set "BASEDIR=%~dp0"

REM Activate the virtual environment from this folder
call "P:\LabX-Global\Scripts\activate.bat"

REM Keep the terminal open
cmd /k
