param(
    [ValidateSet("windows", "linux", IgnoreCase = $true)]
    [string]$Target = "windows"
)

$ErrorActionPreference = "Stop"

$Target = $Target.ToLower()
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

Write-Host "=== Building Text-to-Speech for target: $Target ===" -ForegroundColor Cyan

if (-not (Get-Command pyinstaller -ErrorAction SilentlyContinue)) {
    Write-Host "PyInstaller not found. Installing via pip..." -ForegroundColor Yellow
    pip install pyinstaller
}

$IconFlag = ""
if (Test-Path "tts.ico") {
    if ($Target -eq "windows") {
        $IconFlag = '--icon=tts.ico --add-data "tts.ico;."'
    } else {
        $IconFlag = '--icon=tts.ico --add-data "tts.ico:."'
    }
}

switch ($Target) {
    "windows" {
        Write-Host "Building Windows standalone executable..." -ForegroundColor Green
        Invoke-Expression "pyinstaller --noconfirm --onefile --windowed --name `"TextToSpeech`" $IconFlag tts.py"
        Write-Host "Build complete: dist/TextToSpeech.exe" -ForegroundColor Green
    }
    "linux" {
        Write-Host "Building Linux executable..." -ForegroundColor Green
        Invoke-Expression "pyinstaller --noconfirm --onefile --windowed --name `"TextToSpeech`" $IconFlag tts.py"
        Write-Host "Build complete: dist/TextToSpeech" -ForegroundColor Green
    }
}
