#!/bin/bash

# Instalar dependencias necesarias
apt-get update && apt-get install -y git curl software-properties-common build-essential

# Instalar Go si no está
if ! command -v go &> /dev/null; then
    echo "Instalando Go..."
    add-apt-repository ppa:longsleep/golang-backports -y
    apt-get update && apt-get install -y golang-go
fi

# Clonar Geth si no existe
if [ ! -d "/nucleo/go-ethereum" ]; then
    cd /nucleo
    git clone https://github.com/ethereum/go-ethereum.git
fi

# Compilar Geth
cd /nucleo/go-ethereum
make geth

# Inicializar el nodo con genesis.json
./build/bin/geth init /nucleo/test2network/genesis.json --datadir /nucleo/test2network

# Lanzar el nodo con los flags correctos
exec ./build/bin/geth --networkid 99118822 \
    --http \
    --http.addr 0.0.0.0 \
    --http.port 8545 \
    --http.api personal,eth,net,web3 \
    --http.corsdomain="*" \
    --http.vhosts="*" \
    --datadir /nucleo/test2network

