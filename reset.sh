#!/bin/bash

echo "🧹 Deteniendo y eliminando contenedores..."
docker-compose down -v --remove-orphans

echo "🧼 Eliminando contenedores antiguos si existen..."
docker rm -f historia_web historia_db 2>/dev/null

echo "🗑️ Eliminando imagen de Flask si existe..."
docker rmi historia_clinica_bfa_web 2>/dev/null

echo "🚀 Reconstruyendo y levantando el entorno..."
docker-compose up --build
