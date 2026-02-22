# Manual Checks

These scripts are optional local diagnostics and are intentionally outside
`test_*.py` naming so they are not auto-discovered by `manage.py test`.

## Scripts
- `scripts/manual_checks/risk_guard_checks.py`
- `scripts/manual_checks/risk_scenario_checks.py`
- `scripts/manual_checks/supabase_connection_check.py`

## Usage
```powershell
python scripts/manual_checks/risk_guard_checks.py
python scripts/manual_checks/risk_scenario_checks.py
$env:SUPABASE_DATABASE_URL = "postgresql://..."
python scripts/manual_checks/supabase_connection_check.py
```
