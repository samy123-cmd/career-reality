#!/usr/bin/env bash
# Run Django management commands locally with .env loaded.
set -euo pipefail
cd "$(dirname "$0")/.."

if [[ -f .env ]]; then
  set -a
  # shellcheck disable=SC1091
  source .env
  set +a
fi

export DEBUG="${DEBUG:-True}"
export SECRET_KEY="${SECRET_KEY:-local-dev-only-change-in-production}"

exec python3 manage.py "$@"
