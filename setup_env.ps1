<#
.SYNOPSIS
    Automated environment setup script for Exam Timetable Scheduler (AAD Project).
.DESCRIPTION
    Checks Python installation, verifies Tkinter support, creates/activates a virtual environment (.venv),
    and offers an interactive menu to launch the project directly on any Windows PC.
#>

[CmdletBinding()]
param(
    [switch]$SkipMenu
)

function Write-Info {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Cyan
}

function Write-Success {
    param([string]$Message)
    Write-Host "[OK]   $Message" -ForegroundColor Green
}

function Write-WarningMsg {
    param([string]$Message)
    Write-Host "[WARN] $Message" -ForegroundColor Yellow
}

function Write-ErrorMsg {
    param([string]$Message)
    Write-Host "[ERR]  $Message" -ForegroundColor Red
}

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "     Exam Timetable Scheduler - Environment Setup         " -ForegroundColor White
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Detect Python Command
$PythonCmd = $null
$candidates = @("python", "py", "python3")

foreach ($cmd in $candidates) {
    if (Get-Command $cmd -ErrorAction SilentlyContinue) {
        $PythonCmd = $cmd
        break
    }
}

if (-not $PythonCmd) {
    Write-ErrorMsg "Python was not found on this system."
    Write-Host ""
    Write-Host "Please install Python 3 (ensure 'Add Python to PATH' and 'tcl/tk and IDLE' are checked):" -ForegroundColor Yellow
    Write-Host "  👉 Windows Package Manager: winget install Python.Python.3.11" -ForegroundColor Yellow
    Write-Host "  👉 Or official installer:   https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host ""
    exit 1
}

$pyVersion = & $PythonCmd --version 2>&1
Write-Success "Found Python command: '$PythonCmd' ($pyVersion)"

# 2. Check Tkinter Support
Write-Info "Verifying Tkinter GUI support..."
$tkCheck = & $PythonCmd -c "import tkinter; print('OK')" 2>$null
if ($tkCheck -match "OK") {
    Write-Success "Tkinter GUI module is available."
} else {
    Write-WarningMsg "Tkinter is not found in this Python installation."
    Write-Host "       (Note: GUI visualizer needs Tkinter. On Windows, rerun Python installer and select 'tcl/tk and IDLE'.)" -ForegroundColor DarkYellow
}

# 3. Setup Virtual Environment
$venvPath = Join-Path -Path $PSScriptRoot -ChildPath ".venv"
$venvPython = Join-Path -Path $venvPath -ChildPath "Scripts\python.exe"
$venvActivate = Join-Path -Path $venvPath -ChildPath "Scripts\Activate.ps1"

if (-not (Test-Path $venvPython)) {
    Write-Info "Creating virtual environment (.venv)..."
    & $PythonCmd -m venv $venvPath
    if (-not (Test-Path $venvPython)) {
        Write-ErrorMsg "Failed to create virtual environment."
        exit 1
    }
    Write-Success "Virtual environment created at: $venvPath"
} else {
    Write-Success "Existing virtual environment found at: $venvPath"
}

# 4. Check dependencies (Project uses standard library; checks requirements.txt if present)
$reqPath = Join-Path -Path $PSScriptRoot -ChildPath "requirements.txt"
if (Test-Path $reqPath) {
    # Check if requirements.txt actually has non-comment packages
    $nonEmptyLines = Get-Content $reqPath | Where-Object { $_ -match '\S' -and -not ($_ -match '^\s*#') }
    if ($nonEmptyLines) {
        Write-Info "Installing dependencies from requirements.txt..."
        & $venvPython -m pip install -r $reqPath
    } else {
        Write-Success "No external third-party packages required (Standard Library only)."
    }
}

Write-Host "`nEnvironment setup is complete!" -ForegroundColor Green
Write-Host "Python Path: $venvPython" -ForegroundColor Gray

if ($SkipMenu) {
    exit 0
}

# 5. Interactive Launch Options
Write-Host "`nSelect an option to run:" -ForegroundColor Cyan
Write-Host "  [1] Launch GUI Visualizer (timetable_visualizer.py)" -ForegroundColor White
Write-Host "  [2] Launch Terminal Visualizer (terminal_visualizer.py)" -ForegroundColor White
Write-Host "  [3] Exit" -ForegroundColor White

$choice = Read-Host "`nEnter your choice (1/2/3) [Default: 1]"
if ([string]::IsNullOrWhiteSpace($choice)) {
    $choice = "1"
}

switch ($choice) {
    "1" {
        Write-Info "Launching GUI Visualizer..."
        & $venvPython (Join-Path -Path $PSScriptRoot -ChildPath "timetable_visualizer.py")
    }
    "2" {
        Write-Info "Launching Terminal Visualizer..."
        & $venvPython (Join-Path -Path $PSScriptRoot -ChildPath "terminal_visualizer.py")
    }
    default {
        Write-Info "Exiting. You can activate the venv anytime with: .\.venv\Scripts\Activate.ps1"
    }
}
