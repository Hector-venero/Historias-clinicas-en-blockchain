#!/bin/bash

echo "🧹 Eliminando contenedor historia_web si existe..."
docker rm -f historia_web 2>/dev/null || echo "No se encontró un contenedor en ejecución con el nombre historia_web."

echo "🔧 Reconstruyendo contenedor historia_web..."
docker-compose build web

echo "🚀 Levantando contenedor historia_web conectado a la red historia_net..."
docker-compose up -d web

echo "✅ Contenedor historia_web reiniciado y en ejecución."
