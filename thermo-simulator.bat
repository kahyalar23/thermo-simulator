@echo off
chcp 65001 >nul
title Thermodynamic Cycle Simulator - ITU
color 0A
echo.
echo ========================================
echo   THERMODYNAMIC CYCLE SIMULATOR
echo   ITU Civil & Mechanical Engineering
echo ========================================
echo.
echo Usage: thermo-simulator [options]
echo.
echo Options:
echo   --cycle all|carnot|brayton|rankine
echo   --T_hot N          (Carnot hot source K)
echo   --T_cold N         (Carnot cold sink K)
echo   --T_in N           (Brayton inlet K)
echo   --T_max N          (Brayton max temp K)
echo   --pr N             (Pressure ratio)
echo   --p_high N         (Rankine high pressure MPa)
echo   --p_low N          (Rankine low pressure MPa)
echo   --T_sh N           (Rankine superheat C)
echo   --compare           (Compare all cycles)
echo   --no_plot           (Skip diagram generation)
echo   --debug             (Full state data)
echo   --help              (Show this help)
echo.
echo Examples:
echo   thermo-simulator --cycle all --compare
echo   thermo-simulator --cycle carnot --T_hot 800 --T_cold 300
echo   thermo-simulator --cycle rankine --debug
echo.
echo ========================================
echo.

python "%~dp0main.py" %*

echo.
echo Press any key to exit...
pause >nul
