#Requires -Version 5.1
<#
.SYNOPSIS
  Launch Smart Hub Prod (The Scoop 52 Streamlit app).

.DESCRIPTION
  Creates/activates a local venv, installs dependencies, ensures secrets exist,
  and runs the app with APP_ENV=production.

.EXAMPLE
  .\launch.ps1

.EXAMPLE
  .\launch.ps1 -Port 8502 -SkipInstall

.EXAMPLE
  .\launch.ps1 -RecreateVenv

.EXAMPLE
  .\launch.ps1 -SkipSmokeTest
#>
param(
    [int]$Port = 8501,
    [switch]$SkipInstall,
    [switch]$RecreateVenv,
    [switch]$SkipSmokeTest,
    [switch]$QuickSmokeTest
)

$ErrorActionPreference = "Stop"
$ProjectRoot = (Resolve-Path $PSScriptRoot).Path
Set-Location $ProjectRoot

function Find-Python {
    foreach ($cmd in @("py", "python", "python3")) {
        $exe = Get-Command $cmd -ErrorAction SilentlyContinue
        if ($exe) {
            return $exe.Source
        }
    }
    throw "Python not found. Install Python 3.11+ and ensure it is on PATH."
}

function Test-VenvHealthy {
    param(
        [string]$VenvPath,
        [string]$ExpectedRoot
    )

    $venvPython = Join-Path $VenvPath "Scripts\python.exe"
    $pyvenvCfg = Join-Path $VenvPath "pyvenv.cfg"

    if (-not (Test-Path $venvPython) -or -not (Test-Path $pyvenvCfg)) {
        return $false
    }

    $cfg = Get-Content $pyvenvCfg -Raw
    $normalizedExpected = ($ExpectedRoot -replace '\\', '/').ToLowerInvariant()
    $normalizedCfg = ($cfg -replace '\\', '/').ToLowerInvariant()

    if ($normalizedCfg -notmatch [regex]::Escape($normalizedExpected)) {
        return $false
    }

    try {
        & $venvPython -c "import sys; print(sys.executable)" | Out-Null
        return $true
    }
    catch {
        return $false
    }
}

function New-ProjectVenv {
    param(
        [string]$VenvPath,
        [string]$PythonLauncher
    )

    if (Test-Path $VenvPath) {
        Write-Host "Removing stale virtual environment at $VenvPath ..."
        Remove-Item $VenvPath -Recurse -Force
    }

    Write-Host "Creating virtual environment at $VenvPath ..."
    if ($PythonLauncher -match "py(\.exe)?$") {
        & $PythonLauncher -3 -m venv $VenvPath
    }
    else {
        & $PythonLauncher -m venv $VenvPath
    }
}

$pythonLauncher = Find-Python
$venvPath = Join-Path $ProjectRoot "venv"
$venvPython = Join-Path $venvPath "Scripts\python.exe"
$activateScript = Join-Path $venvPath "Scripts\Activate.ps1"

$venvHealthy = Test-VenvHealthy -VenvPath $venvPath -ExpectedRoot $ProjectRoot
if ($RecreateVenv -or -not $venvHealthy) {
    if (-not $venvHealthy -and (Test-Path $venvPath)) {
        Write-Warning "Virtual environment is missing or was copied from another project. Recreating it."
    }
    New-ProjectVenv -VenvPath $venvPath -PythonLauncher $pythonLauncher
}

if (-not (Test-Path $activateScript)) {
    throw "Virtual environment activation script not found: $activateScript"
}

. $activateScript

if (-not $SkipInstall) {
    Write-Host "Installing dependencies from requirements.txt ..."
    & $venvPython -m pip install -r (Join-Path $ProjectRoot "requirements.txt")
}

$secretsDir = Join-Path $ProjectRoot ".streamlit"
$secretsPath = Join-Path $secretsDir "secrets.toml"
$secretsExample = Join-Path $secretsDir "secrets.toml.example"

if (-not (Test-Path $secretsPath)) {
    if (Test-Path $secretsExample) {
        New-Item -ItemType Directory -Force -Path $secretsDir | Out-Null
        Copy-Item $secretsExample $secretsPath
        Write-Warning "Created .streamlit\secrets.toml from example. Edit it with your Supabase and Alpha Vantage keys."
    }
    else {
        Write-Warning "Missing .streamlit\secrets.toml. Copy .streamlit\secrets.toml.example and fill in your keys."
    }
}

$env:APP_ENV = "production"

if (-not $SkipSmokeTest) {
    Write-Host ""
    Write-Host "Running pre-launch smoke tests ..."
    $smokeArgs = @("admin_tools/smoke_test.py")
    if ($QuickSmokeTest) {
        $smokeArgs += "--quick"
    }
    & $venvPython @smokeArgs
    if ($LASTEXITCODE -ne 0) {
        throw "Smoke tests failed (exit $LASTEXITCODE). Fix issues or use -SkipSmokeTest to bypass."
    }
    Write-Host "Smoke tests passed."
}

Write-Host ""
Write-Host "Starting Smart Hub Prod (APP_ENV=production) at http://localhost:$Port"
Write-Host "Press Ctrl+C to stop."
Write-Host ""

& $venvPython -m streamlit run (Join-Path $ProjectRoot "app.py") --server.port $Port
