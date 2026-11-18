@echo off
title Pixel Runner - 2D Game 01
cd /d "%~dp0"
python main.py
if errorlevel 1 (
    echo.
    echo Xatolik yuz berdi. Pygame o'rnatilganligini tekshiring: pip install pygame
    pause
)
