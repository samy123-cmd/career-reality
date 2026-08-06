#!/usr/bin/env bash
set -euo pipefail

ROLE="${1:-web}"
PORT="${PORT:-8000}"
WORKERS="${WEB_CONCURRENCY:-2}"
TIMEOUT="${GUNICORN_TIMEOUT:-60}"

case "$ROLE" in
  web)
    if [[ "${RUN_DB_MIGRATE:-True}" =~ ^([Tt]rue|1|yes|YES)$ ]]; then
      echo "[entrypoint] migrate"
      python manage.py migrate --noinput
    fi
    if [[ "${RUN_COLLECTSTATIC:-True}" =~ ^([Tt]rue|1|yes|YES)$ ]]; then
      echo "[entrypoint] collectstatic"
      python manage.py collectstatic --noinput
    fi
    echo "[entrypoint] gunicorn on :${PORT} workers=${WORKERS}"
    exec gunicorn config.wsgi:application \
      --bind "0.0.0.0:${PORT}" \
      --workers "${WORKERS}" \
      --timeout "${TIMEOUT}" \
      --access-logfile - \
      --error-logfile - \
      --capture-output
    ;;
  worker|cron)
    echo "[entrypoint] cron runner"
    exec /app/deploy/cron-runner.sh
    ;;
  shell)
    exec bash
    ;;
  *)
    echo "Unknown role: $ROLE (expected web|cron|shell)" >&2
    exit 1
    ;;
esac
