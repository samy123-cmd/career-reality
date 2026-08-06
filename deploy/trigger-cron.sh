#!/usr/bin/env bash
# One-shot cron wrappers usable from any external scheduler (Fly, cron-job.org, systemd).
# Prefer deploy/cron-runner.sh on Fly. These curl endpoints keep CRON_SECRET auth.
set -euo pipefail

BASE_URL="${BASE_URL:-https://www.careerreality.in}"
TOKEN="${CRON_SECRET:?CRON_SECRET required}"

auth_hdr=(-H "Authorization: Bearer ${TOKEN}")

case "${1:-}" in
  warm)
    curl -fsS "${auth_hdr[@]}" "${BASE_URL}/internal/cron/warm-cache/"
    ;;
  freshness-light)
    curl -fsS "${auth_hdr[@]}" "${BASE_URL}/internal/cron/freshness/?warm_cache=True"
    ;;
  freshness-nightly)
    curl -fsS "${auth_hdr[@]}" \
      "${BASE_URL}/internal/cron/freshness/?commit_refresh=True&strict_freshness=True&warm_cache=True&fetch_limit=2&refresh_articles=True&prune_ai=True&bootstrap_august=True"
    ;;
  digest)
    curl -fsS "${auth_hdr[@]}" "${BASE_URL}/internal/cron/weekly-digest/"
    ;;
  layoffs)
    curl -fsS "${auth_hdr[@]}" "${BASE_URL}/internal/cron/layoff-alerts/"
    ;;
  index)
    curl -fsS "${auth_hdr[@]}" "${BASE_URL}/internal/cron/refresh-career-index/"
    ;;
  *)
    echo "Usage: $0 {warm|freshness-light|freshness-nightly|digest|layoffs|index}" >&2
    exit 1
    ;;
esac
