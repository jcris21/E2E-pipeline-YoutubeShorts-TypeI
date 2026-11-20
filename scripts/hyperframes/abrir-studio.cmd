@echo off
REM Abre HyperFrames Studio para este proyecto (preview en vivo + edicion).
REM Requiere Node.js 22+ instalado en Windows.
cd /d "%~dp0"
where node >nul 2>nul
if errorlevel 1 (
  echo [ERROR] No se encontro Node.js. Instala Node 22+ desde https://nodejs.org y vuelve a ejecutar.
  pause
  exit /b 1
)
echo Iniciando HyperFrames Studio en http://localhost:3002 ...
npx --yes hyperframes@0.9.71 preview --port 3002
pause
