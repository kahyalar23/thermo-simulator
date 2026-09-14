@echo off
chcp 65001 >nul
title Thermodynamic Cycle Simulator - ITU
color 0A

REM Get script directory
set "SCRIPT_DIR=%~dp0"

REM Check if python exists
where python >nul 2>&1
if errorlevel 1 (
    echo.
    echo HATA: Python bulunamadi! Lütfen Python 3.9+ kurun ve PATH'e ekleyin.
    echo.
    pause
    exit /b 1
)

REM If no arguments, show menu
if "%~1"=="" (
    call :MENU
    goto :EOF
)

REM Run with arguments
python "%SCRIPT_DIR%main.py" %*
if errorlevel 1 (
    echo.
    echo HATA: Program hatali sonlandi. Detaylar icin --debug kullanin.
)

echo.
echo Devam etmek icin bir tusa basin...
pause >nul
exit /b

:MENU
cls
echo.
echo ========================================
echo   THERMODYNAMIC CYCLE SIMULATOR
echo   ITU Civil ^& Mechanical Engineering
echo ========================================
echo.
echo  1. Carnot Cycle (T_H=800, T_C=300)
echo  2. Brayton Cycle (rp=10)
echo  3. Rankine Cycle (p_H=10, p_L=0.05)
echo  4. All Cycles + Compare
echo  5. Carnot + Debug
echo  6. Rankine + Debug
echo  7. Custom Parameters
echo  0. Exit
echo.
echo ========================================
echo.

set /p CHOICE="Seciminiz (0-7): "

if "%CHOICE%"=="1" python "%SCRIPT_DIR%main.py" --cycle carnot --T_hot 800 --T_cold 300
if "%CHOICE%"=="2" python "%SCRIPT_DIR%main.py" --cycle brayton --pr 10
if "%CHOICE%"=="3" python "%SCRIPT_DIR%main.py" --cycle rankine --p_high 10 --p_low 0.05 --T_sh 500
if "%CHOICE%"=="4" python "%SCRIPT_DIR%main.py" --cycle all --compare
if "%CHOICE%"=="5" python "%SCRIPT_DIR%main.py" --cycle carnot --T_hot 800 --T_cold 300 --debug
if "%CHOICE%"=="6" python "%SCRIPT_DIR%main.py" --cycle rankine --p_high 10 --p_low 0.05 --debug

if "%CHOICE%"=="7" (
    echo.
    echo Custom Parameters:
    set /p CYC="Cycle (carnot/brayton/rankine/all): "
    if "%CYC%"=="carnot" (
        set /p TH="T_hot (K): "
        set /p TC="T_cold (K): "
        python "%SCRIPT_DIR%main.py" --cycle carnot --T_hot %TH% --T_cold %TC%
    )
    if "%CYC%"=="brayton" (
        set /p PR="Pressure ratio: "
        set /p TIN="T_inlet (K): "
        set /p TMAX="T_max (K): "
        python "%SCRIPT_DIR%main.py" --cycle brayton --pr %PR% --T_in %TIN% --T_max %TMAX%
    )
    if "%CYC%"=="rankine" (
        set /p PH="p_high (MPa): "
        set /p PL="p_low (MPa): "
        set /p TSH="T_superheat (C): "
        python "%SCRIPT_DIR%main.py" --cycle rankine --p_high %PH% --p_low %PL% --T_sh %TSH%
    )
    if "%CYC%"=="all" (
        python "%SCRIPT_DIR%main.py" --cycle all --compare
    )
)

if "%CHOICE%"=="0" exit /b

echo.
echo Devam etmek icin bir tusa basin...
pause >nul
goto MENU