#!/usr/bin/env bash
# Pre-push visual gate: verify all 10 feature pages return 200 and load premium CSS shell.
set -euo pipefail

BASE_URL="${BASE_URL:-http://127.0.0.1:8000}"
FAIL=0

check_url() {
  local path="$1"
  local label="$2"
  local html
  html="$(curl -sf "$BASE_URL$path" || true)"
  if [[ -z "$html" ]]; then
    echo "FAIL $label — no response from $path"
    FAIL=1
    return
  fi
  if ! grep -q 'feature-product.css' <<< "$html"; then
    echo "FAIL $label — missing feature-product.css"
    FAIL=1
  fi
  if ! grep -qE 'az-calc-card|cr-tool-card' <<< "$html"; then
    echo "FAIL $label — missing az-calc-card or cr-tool-card shell"
    FAIL=1
  fi
  if grep -q 'HTTP 404' <<< "$html"; then
    echo "FAIL $label — 404"
    FAIL=1
  fi
  echo "OK   $label ($path)"
}

echo "Checking feature pages at $BASE_URL ..."

check_url "/tools/salary-reality-engine/" "Salary Reality Engine"
check_url "/tools/offer-analyzer/" "Offer Analyzer"
check_url "/tools/stay-vs-switch/" "Stay vs Switch"
check_url "/tools/ai-career-impact/" "AI Career Impact"
check_url "/tools/next-career-move/" "Next Career Move"
check_url "/tools/ask/" "Ask CareerReality"

# Dashboard pages require auth — check login redirect or 200
for path in "/pro/my-career-reality/" "/pro/progression/" "/pro/risk-radar/" "/pro/career-profile/"; do
  code="$(curl -s -o /dev/null -w '%{http_code}' "$BASE_URL$path")"
  if [[ "$code" != "200" && "$code" != "302" ]]; then
    echo "FAIL dashboard $path — HTTP $code"
    FAIL=1
  else
    echo "OK   dashboard $path — HTTP $code"
  fi
done

if [[ "$FAIL" -ne 0 ]]; then
  echo ""
  echo "Preview gate FAILED. Fix issues before pushing."
  exit 1
fi

echo ""
echo "Preview gate passed. Run browser check at 375px and 1280px before push."
