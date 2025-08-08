#!/usr/bin/env bash
set -euo pipefail

# Gestor del entorno: levantar/instalar modelo, parar, reiniciar, limpiar y ver logs

PROJECT_ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEFAULT_MODEL="mistral"

dc() {
  # wrapper por si en algunos entornos se usa docker-compose
  if command -v docker &>/dev/null; then
    docker compose "$@"
  else
    echo "Docker no está instalado en PATH" >&2
    exit 1
  fi
}

print_urls() {
  echo
  echo "Servicios:"
  echo "- n8n:     http://localhost:5678"
  echo "- client:  http://localhost:5173"
  echo "- backend: http://localhost:3000"
  echo "- ollama:  http://localhost:11434"
  echo
}

wait_for_ollama() {
  # Espera a que el contenedor de ollama acepte comandos
  local retries=20
  local delay=2
  echo "Esperando a que Ollama esté listo..."
  for ((i=1; i<=retries; i++)); do
    if dc exec -T ollama ollama --version >/dev/null 2>&1; then
      echo "Ollama listo."
      return 0
    fi
    sleep "$delay"
  done
  echo "Timeout esperando a Ollama" >&2
  return 1
}

cmd_up() {
  # Levanta todos los servicios; opcionalmente instala un modelo: ./setup.sh up llama3
  local model="${1:-}" 
  echo "Levantando servicios en segundo plano..."
  dc up -d
  print_urls
  if [[ -n "$model" ]]; then
    echo "Instalando modelo solicitado: $model"
    dc up -d ollama
    wait_for_ollama
    dc exec -T ollama ollama pull "$model"
    echo "Modelo '$model' instalado."
  fi
}

cmd_model_install() {
  # Instala/pullear un modelo en el contenedor de Ollama
  local model="${1:-}" 
  if [[ -z "$model" ]]; then
    echo "Uso: $0 model install <nombre_modelo>" >&2
    exit 2
  fi
  dc up -d ollama
  wait_for_ollama
  echo "Descargando modelo: $model"
  dc exec -T ollama ollama pull "$model"
  echo "Modelo '$model' instalado."
}

cmd_model_list() {
  dc up -d ollama
  wait_for_ollama
  echo "Modelos instalados:"
  dc exec -T ollama ollama list
}

cmd_stop() {
  # Para servicios; por defecto todos. Ej: ./setup.sh stop [service]
  local svc="${1:-}"
  if [[ -n "$svc" ]]; then
    echo "Parando servicio: $svc"
    dc stop "$svc"
  else
    echo "Parando todos los servicios..."
    dc stop
  fi
}

cmd_rebuil() {
  local svc="${1:-}"
  local model="${1:-}" 
  echo "Recontruyendo en segundo plano..."
  dc up --build -d
  print_urls
}

cmd_restart() {
  # Reinicia servicios; por defecto todos. Ej: ./setup.sh restart [service]
  local svc="${1:-}"
  if [[ -n "$svc" ]]; then
    echo "Reiniciando servicio: $svc"
    dc restart "$svc"
  else
    echo "Reiniciando todos los servicios..."
    dc restart
  fi
}

cmd_clean() {
  # Limpieza: soft (down) o hard (down -v + prune opcional)
  local mode="${1:-soft}"
  case "$mode" in
    soft)
      echo "Bajando contenedores (sin borrar volúmenes)..."
      dc down
      ;;
    hard)
      echo "Bajando contenedores y borrando volúmenes..."
      dc down -v
      read -rp "¿Eliminar imágenes sin usar (docker image prune -f)? [s/N] " ans
      if [[ "${ans:-N}" =~ ^[sS]$ ]]; then
        docker image prune -f
      fi
      ;;
    *)
      echo "Uso: $0 clean [soft|hard]" >&2
      exit 2
      ;;
  esac
}

cmd_logs() {
  # Logs por servicio: ./setup.sh logs <service> [-f]
  if [[ $# -lt 1 ]]; then
    echo "Uso: $0 logs <service> [-f]" >&2
    exit 2
  fi
  local svc="$1"; shift || true
  dc logs "$svc" "$@"
}

cmd_status() {
  dc ps
}

show_help() {
  cat <<EOF
Uso: $0 <comando> [opciones]

Comandos:
  up [modelo]           Levanta todos los servicios (y opcionalmente instala un modelo en Ollama).
  model install <m>     Instala (pull) el modelo <m> dentro del contenedor de Ollama.
  model list            Lista los modelos instalados en Ollama.
  stop [servicio]       Detiene un servicio o todos (si no se especifica).
  restart [servicio]    Reinicia un servicio o todos.
  clean [soft|hard]     Elimina contenedores (soft) o contenedores+volúmenes (hard); con opción de prune.
  logs <servicio> [-f]  Muestra logs de un servicio (use -f para seguir).
  status                Muestra el estado de los servicios (docker compose ps).

Ejemplos:
  $0 up                  # levanta todo
  $0 up llama3           # levanta todo e instala llama3
  $0 model install mistral:latest
  $0 model list
  $0 stop backend
  $0 build
  $0 restart
  $0 clean hard
  $0 logs ollama -f
  $0 status
EOF
}

main() {
  if [[ $# -eq 0 ]]; then
    show_help
    exit 0
  fi

  local cmd="$1"; shift || true
  case "$cmd" in
    up)
      cmd_up "${1:-}"
      ;;
    model)
      local sub="${1:-}"; shift || true
      case "$sub" in
        install) cmd_model_install "${1:-}" ;;
        list)    cmd_model_list ;;
        *) echo "Subcomando inválido para 'model'" >&2; show_help; exit 2 ;;
      esac
      ;;
    stop)
      cmd_stop "${1:-}"
      ;;
    build)
      cmd_rebuil "${1:-}"
      ;;
    restart)
      cmd_restart "${1:-}"
      ;;
    clean)
      cmd_clean "${1:-soft}"
      ;;
    logs)
      cmd_logs "$@"
      ;;
    status)
      cmd_status
      ;;
    help|-h|--help)
      show_help
      ;;
    *)
      echo "Comando no reconocido: $cmd" >&2
      show_help
      exit 2
      ;;
  esac
}

main "$@"