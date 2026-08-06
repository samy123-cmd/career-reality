# Skill verification report (2026-08-06)

Ran all eight project skills in one pass: structure checks, four parallel skill-follow agents, then Django command smoke tests after local `migrate`.

## Verdict

| Skill | Structure | Agent follow-through | Runtime smoke | Overall |
|-------|-----------|----------------------|---------------|---------|
| `career-reality-overview` | PASS | PASS | N/A (map skill) | **PASS** |
| `publish-career-article` | PASS | PASS | quality/seo/upgrade cmds PASS | **PASS** |
| `seo-gsc-hygiene` | PASS | PASS | seo_audit + draft_redirect_losers PASS | **PASS** |
| `cache-and-deploy` | PASS | PASS | warm_page_cache 16/16 PASS | **PASS** |
| `ai-pulse-ops` | PASS | PASS | fetch_ai_news + prune dry-run PASS | **PASS** |
| `frontend-cr-design` | PASS | PASS | N/A (filesystem/CSS) | **PASS** |
| `content-freshness` | PASS | PASS | harden/upgrade cmds PASS | **PASS** |
| `release-preflight` | PASS | PASS | preflight (+ freshness) PASS | **PASS** |

**Command smokes: 10/10 passed** (`preflight_release`, `--check-freshness`, `prune_ai_news`, `harden_content_quality`, `draft_redirect_losers`, `quality_audit`, `seo_audit`, `generate_upgrade_sheet`, `warm_page_cache --article-limit 0`, `fetch_ai_news --limit 1`).

## Fixes applied after testing

Skills were tightened where verification found drift:

- Companies vs analyzer ownership clarified
- August vs July seed helper patterns clarified
- Sitemap exclusion noted as automatic; category vercel mirrors called out
- `EDGE_CACHE_DENY_PREFIXES` separated from `EDGE_CACHE_RULES`
- `prune_ai_news` dry-run / cron→maintenance path documented
- Token naming (`--cr-*` vs `--space-*` / `--radius-*`) corrected
- Removed nonexistent `apply_release_content_fixes` and missing `.ps1` bundle as required steps

## Limits of this environment

- Local SQLite had no seeded articles (audits correctly reported 0 published).
- `preflight_release` correctly flagged `DEBUG=True` / missing secure cookies for this test env (expected without `--strict` exit 0).
- Skills themselves are instruction packages — “running” them means agents following them + verifying referenced commands/files, which this pass did.
