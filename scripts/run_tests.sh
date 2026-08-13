#!/usr/bin/env bash
# Canonical test entrypoint.
#
# `python manage.py test` with no labels currently fails during unittest
# discovery ("'tests' module incorrectly imported from analyzer/tests"), so the
# app labels are passed explicitly. Any new local app must be added here.
set -euo pipefail

cd "$(dirname "$0")/.."

export DEBUG="${DEBUG:-True}"
export SECRET_KEY="${SECRET_KEY:-dev-test-key}"
export DATABASE_URL="${DATABASE_URL:-}"

PYTHON="${PYTHON:-.venv/bin/python}"
[ -x "$PYTHON" ] || PYTHON="python3"

APPS=(
  core
  content
  analyzer
  ainews
  accounts
  payments
  companies
  search
)

echo "Running test suite across ${#APPS[@]} apps..."
exec "$PYTHON" manage.py test "${APPS[@]}" "$@"
