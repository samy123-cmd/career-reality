#!/usr/bin/env bash
# Lightweight in-process scheduler replacing Vercel Cron.
# Prefer invoking management commands directly (no HTTP hop, no cold start).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

log() { echo "[cron $(date -u +%Y-%m-%dT%H:%M:%SZ)] $*"; }

run_cmd() {
  local label="$1"; shift
  log "START $label"
  if python manage.py "$@"; then
    log "OK $label"
  else
    log "FAIL $label (exit $?)"
  fi
}

# Align with former vercel.json schedules (Asia/Kolkata wall clock via TZ).
export TZ="${TZ:-Asia/Kolkata}"

last_warm_hour=""
last_fresh_hour=""
last_nightly_day=""
last_digest_week=""
last_layoff_hour=""
last_index_month=""

log "cron runner online (TZ=$TZ)"

while true; do
  now_h="$(date +%H)"
  now_m="$(date +%M)"
  now_dow="$(date +%u)"   # 1=Mon
  now_dom="$(date +%d)"
  now_mon="$(date +%m)"
  stamp_h="$(date +%Y%m%d%H)"
  stamp_d="$(date +%Y%m%d)"
  stamp_w="$(date +%G%V)"
  stamp_mo="$(date +%Y%m)"

  # Every 4 hours at :00 — warm cache (was vercel warm-cache)
  if [[ "$now_m" == "00" && $((10#$now_h % 4)) -eq 0 && "$last_warm_hour" != "$stamp_h" ]]; then
    last_warm_hour="$stamp_h"
    run_cmd warm_page_cache warm_page_cache --article-limit "${CRON_ARTICLE_WARM_LIMIT:-20}"
  fi

  # Every 6 hours at :00 — light freshness + layoff alerts
  if [[ "$now_m" == "00" && $((10#$now_h % 6)) -eq 0 && "$last_fresh_hour" != "$stamp_h" ]]; then
    last_fresh_hour="$stamp_h"
    run_cmd light_freshness run_production_maintenance --fetch-limit "${CRON_FETCH_LIMIT_LIGHT:-2}" --warm-cache
    run_cmd layoff_alerts send_layoff_alerts
  fi

  # 02:30 daily — committed refresh (was vercel nightly freshness)
  if [[ "$now_h$now_m" == "0230" && "$last_nightly_day" != "$stamp_d" ]]; then
    last_nightly_day="$stamp_d"
    run_cmd nightly_freshness run_production_maintenance \
      --fetch-limit "${CRON_FETCH_LIMIT_NIGHTLY:-2}" \
      --commit-refresh \
      --strict-freshness \
      --warm-cache \
      --refresh-articles \
      --prune-ai \
      --bootstrap-august
  fi

  # Monday 09:00 — weekly digest
  if [[ "$now_dow" == "1" && "$now_h$now_m" == "0900" && "$last_digest_week" != "$stamp_w" ]]; then
    last_digest_week="$stamp_w"
    run_cmd weekly_digest send_weekly_digest
  fi

  # 1st of month 03:00 — career index
  if [[ "$now_dom" == "01" && "$now_h$now_m" == "0300" && "$last_index_month" != "$stamp_mo" ]]; then
    last_index_month="$stamp_mo"
    run_cmd career_index refresh_career_index
  fi

  sleep 30
done
