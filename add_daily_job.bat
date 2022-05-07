SCHTASKS /CREATE /SC DAILY /TN "Collect getty statistics" /TR "%cd%\run.bat > %cd%\log.txt" /ST 14:40
