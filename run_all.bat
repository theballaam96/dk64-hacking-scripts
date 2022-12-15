@echo off
cls
setlocal EnableDelayedExpansion
for /f %%a in ('copy /Z "%~dpf0" nul') do set "CR=%%a"

echo Started: %date% %time%
echo Started: %date% %time%
echo.

:: Delete ROM name in file
if exist "ROM" (
    DEL "ROM"
)
:: Open file dialog for ROM
set dialog="about:<input type=file id=FILE><script>FILE.click();new ActiveXObject
set dialog=%dialog%('Scripting.FileSystemObject').GetStandardStream(1).WriteLine(FILE.value);
set dialog=%dialog%close();resizeTo(0,0);</script>"

for /f "tokens=* delims=" %%p in ('mshta.exe %dialog%') do set "file=%%p"
echo %file% >> ROM

cd scripts
for /r %%i in (*.py) do if NOT %%~nxi == lib.py call :runscript %%~nxi, %%i
cd ../
@REM for /r %%i in (scripts/*) do echo %%i

:: Delete ROM name in file
if exist "ROM" (
    DEL "ROM"
)

:finish

echo.
echo Completed: %date% %time%
echo Completed: %date% %time%
exit /b

:runscript
<nul set /p=%~1!CR!
call :setstart
python %~2 >> ../build.log
call :setfinish runtime
echo %~1 [32mDONE[0m (%runtime%)
exit /B 0

:setstart
set "startTime=%time: =0%"
exit /B 0

:setfinish
set "endTime=%time: =0%"
set "end=!endTime:%time:~8,1%=%%100)*100+1!"  &  set "start=!startTime:%time:~8,1%=%%100)*100+1!"
set /A "elap=((((10!end:%time:~2,1%=%%100)*60+1!%%100)-((((10!start:%time:~2,1%=%%100)*60+1!%%100), elap-=(elap>>31)*24*60*60*100"
set /A "cc=elap%%100+100,elap/=100,ss=elap%%60+100,elap/=60,mm=elap%%60+100,hh=elap/60+100"
set "%~1=%hh:~1%%time:~2,1%%mm:~1%%time:~2,1%%ss:~1%%time:~8,1%%cc:~1%"
exit /B 0