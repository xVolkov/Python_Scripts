@echo off

REM Run blackScreenTest.py script and capture the output
blackScreenTest.py
echo %ERRORLEVEL%

REM Check the .py script return value and echo the result
IF %ERRORLEVEL% equ 0 (
	echo Screen is lit *** PASS ***

) ELSE IF %ERRORLEVEL% equ 2 (
	echo Screen is NOT lit *** FAIL ***

) ELSE IF %ERRORLEVEL% equ 3 (
	echo No Arduino board detected, check connection between Arduino board and system *** FAIL ***
	
) ELSE IF %ERRORLEVEL% equ 4 (
	echo No light sensor detected, check connection between Arduino board and light sensor *** FAIL ***

) ELSE (
	echo ERROR, Python script failed to run *** FAIL ***
)