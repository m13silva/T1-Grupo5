@echo off
REM Ponemos la carpeta al inicio del PATH
set "PATH=C:\Program Files (x86)\Dev-Cpp\MinGW64\bin;%PATH%"

REM Ahora cualquier ejecutable en esa carpeta tendrá prioridad
mingw32-make.exe -f Makefile.win all
