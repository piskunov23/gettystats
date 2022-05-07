@echo on
SET mypath=%~dp0
cd %mypath%
python src/python/main.py %*
@echo off
REM uncomment if terminal should be cloased 
REM exit
