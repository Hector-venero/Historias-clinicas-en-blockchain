#!/bin/bash

set -e

echo "📦 Instalando dependencias..."
apt-get update && apt-get install -y git curl build-essential software-properties-common

# Instalar Go si no existe
if ! command -v go &> /dev/null; then
    echo "🔧 Instalando Go..."
    add-apt-repository -y ppa:longsleep/golang-backports
    apt-get update && apt-get install -y golang-go
fi

# Clonar Geth si no existe
if [ ! -d "/nucleo/go-ethereum" ]; then
    echo "📥 Clonando Geth..."
    cd /nucleo
    git clone https://github.com/ethereum/go-ethereum.git
fi

echo "⚙️ Compilando Geth..."
cd /nucleo/go-ethereum
make geth

echo "🧱 Inicializando red con genesis.json..."
./build/bin/geth init /nucleo/test2network/genesis.json --datadir /nucleo/test2network

echo "🚀 Lanzando nodo BFA en background..."
exec ./build/bin/geth --networkid 99118822 \
  --http \
  --http.addr 0.0.0.0 \
  --http.port 8545 \
  --http.api eth,net,web3,txpool,debug,engine \
  --http.corsdomain="*" \
  --http.vhosts="*" \
  --datadir /nucleo/test2network
