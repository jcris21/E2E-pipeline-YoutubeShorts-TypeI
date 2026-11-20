#!/usr/bin/env bash
# Abre HyperFrames Studio para el proyecto en la carpeta actual (preview en vivo + edicion).
# Equivalente macOS/Linux de abrir-studio.cmd. Requiere Node.js 22+.
cd "$(dirname "$0")"
if ! command -v node >/dev/null 2>&1; then
  echo "[ERROR] No se encontro Node.js. Instala Node 22+ desde https://nodejs.org"; exit 1
fi
echo "Iniciando HyperFrames Studio en http://localhost:3002 ..."
npx --yes hyperframes@0.9.71 preview --port 3002
