#!/usr/bin/env bash
set -euo pipefail

# Usage: scripts/gunicorn_start.sh [--env-file .env] [--host 0.0.0.0] [--port 8000]

ENV_FILE=""
HOST="0.0.0.0"
PORT="8000"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --env-file)
      ENV_FILE="$2"; shift 2 ;;
    --host)
      HOST="$2"; shift 2 ;;
    --port)
      PORT="$2"; shift 2 ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

if [[ -n "$ENV_FILE" && -f "$ENV_FILE" ]]; then
  set -a
  # shellcheck disable=SC1090
  source "$ENV_FILE"
  set +a
fi

exec gunicorn -c deploy/gunicorn.conf.py -b "$HOST:$PORT" main:app
