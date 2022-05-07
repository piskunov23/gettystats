SCHTASKS /CREATE /SC DAILY /TN "gettystats" /TR "%cd%\run.bat > %cd%\log.txt" /ST 03:00
