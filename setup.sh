#!/bin/bash

docker compose up -d 

echo ""
echo "Contenedores levantados:"
echo "n8n:     http://localhost:5678"
echo "Ollama:  http://localhost:11434"


sleep 5

echo "Instalar el modelo llama3"
docker exect -it n8n-project-ollama-1 ollama pull llama3

echo "Modelo llama3 instalado"