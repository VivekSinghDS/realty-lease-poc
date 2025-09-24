param(
    [string]$ListenHost = "127.0.0.1",
    [int]$Port = 8000,
    [switch]$NoReload
)

$ErrorActionPreference = "Stop"

function Write-Info($msg) { Write-Host "[INFO] $msg" -ForegroundColor Cyan }
function Write-Warn($msg) { Write-Host "[WARN] $msg" -ForegroundColor Yellow }
function Write-Err($msg)  { Write-Host "[ERROR] $msg" -ForegroundColor Red }

try {
    Write-Info "Checking Python availability"

    $pythonExe = $null
    $pythonArgs = @()

    $pythonCmd = Get-Command python -ErrorAction SilentlyContinue
    if ($pythonCmd) {
        $pythonExe = $pythonCmd.Path
    } else {
        $pyCmd = Get-Command py -ErrorAction SilentlyContinue
        if ($pyCmd) {
            $pythonExe = $pyCmd.Path
            $pythonArgs = @("-3.11")
        }
    }

    if (-not $pythonExe) {
        throw "Python 3.11+ not found. Install from https://www.python.org/downloads/"
    }

    # Ensure virtual environment exists
    $venvPython = Join-Path -Path (Resolve-Path ".") -ChildPath ".venv\\Scripts\\python.exe"
    if (-not (Test-Path $venvPython)) {
        Write-Info "Creating virtual environment at .venv"
        & $pythonExe @pythonArgs -m venv .venv
        $venvPython = Join-Path -Path (Resolve-Path ".") -ChildPath ".venv\\Scripts\\python.exe"
    }

    if (-not (Test-Path $venvPython)) {
        throw "Virtual environment Python not found at $venvPython"
    }

    # Upgrade pip and install deps
    Write-Info "Upgrading pip"
    & $venvPython -m pip install --upgrade pip | Out-Null

    Write-Info "Installing requirements"
    & $venvPython -m pip install -r requirements.txt

    # Environment variables: set sensible defaults if absent
    if (-not $env:OPENAI_API_KEY) {
        Write-Warn "OPENAI_API_KEY not set. Set it to enable LLM calls."
    }
    if (-not $env:LLM) {
        $env:LLM = '{"provider":"openai"}'
        Write-Info "LLM not set; defaulting to $env:LLM"
    }
    if (-not $env:ENVIRONMENT) {
        $env:ENVIRONMENT = "development"
        Write-Info "ENVIRONMENT not set; defaulting to $env:ENVIRONMENT"
    }

    $reloadArgs = @()
    if (-not $NoReload) { $reloadArgs = @("--reload") }

    Write-Info "Starting app on http://${ListenHost}:${Port}"
    & $venvPython -m uvicorn app.main:app --host $ListenHost --port $Port $reloadArgs
}
catch {
    Write-Err $_.Exception.Message
    exit 1
}

