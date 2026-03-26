param(
    [switch]$ProductionLike,
    [switch]$RunTests,
    [string]$SecretKey = "local-dev-secret",
    [string]$AllowedHosts = "localhost,127.0.0.1,testserver"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$workspaceRoot = Split-Path -Parent $PSScriptRoot
$pythonExe = Join-Path $workspaceRoot ".venv\Scripts\python.exe"

if (-not (Test-Path $pythonExe)) {
    throw "Python executable not found at $pythonExe. Activate/create .venv first."
}

Push-Location $workspaceRoot
try {
    $env:SECRET_KEY = $SecretKey
    $env:ALLOWED_HOSTS = $AllowedHosts

    if ($ProductionLike) {
        $env:DEBUG = "False"
        $env:SECURE_SSL_REDIRECT = "True"
        $env:SESSION_COOKIE_SECURE = "True"
        $env:CSRF_COOKIE_SECURE = "True"
        $env:SECURE_HSTS_SECONDS = "31536000"
        Write-Host "[Mode] Production-like" -ForegroundColor Cyan
    }
    else {
        $env:DEBUG = "True"
        Write-Host "[Mode] Local development-safe" -ForegroundColor Cyan
    }

    function Invoke-Step {
        param(
            [Parameter(Mandatory = $true)]
            [string]$Name,
            [Parameter(Mandatory = $true)]
            [string[]]$Arguments
        )

        Write-Host "`n==> $Name" -ForegroundColor Yellow
        & $pythonExe @Arguments
        if ($LASTEXITCODE -ne 0) {
            throw "Step failed: $Name"
        }
    }

    Invoke-Step -Name "Apply release content fixes" -Arguments @("manage.py", "apply_release_content_fixes")
    Invoke-Step -Name "Verify AI sources + mark verified" -Arguments @("manage.py", "verify_ai_news_sources", "--commit", "--set-verified")
    Invoke-Step -Name "Strict quality audit" -Arguments @("manage.py", "quality_audit", "--strict")
    Invoke-Step -Name "Strict preflight freshness gate" -Arguments @("manage.py", "preflight_release", "--strict", "--check-freshness")

    if ($RunTests) {
        Invoke-Step -Name "Core test suite" -Arguments @("manage.py", "test", "core", "content", "ainews")
    }

    Write-Host "`n✅ Pre-prod release bundle completed successfully." -ForegroundColor Green
}
finally {
    Pop-Location
}
