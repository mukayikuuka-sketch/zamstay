# ZamStay Startup Script - Run this to start everything
Write-Host @"

╔══════════════════════════════════════════════════════════╗
║                    STARTING ZAMSTAY                      ║
╚══════════════════════════════════════════════════════════╝
"@ -ForegroundColor Cyan

# Check if in virtual environment
if (-not $env:VIRTUAL_ENV) {
    Write-Host "⚠️  Not in virtual environment!" -ForegroundColor Red
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    try {
        . .\myenv\Scripts\Activate.ps1
        Write-Host "✅ Virtual environment activated" -ForegroundColor Green
    } catch {
        Write-Host "❌ Failed to activate virtual environment" -ForegroundColor Red
        Write-Host "Run this first: .\myenv\Scripts\Activate.ps1" -ForegroundColor White
        exit 1
    }
}

# Stop any running server
Write-Host "`n[1] Checking for running servers..." -ForegroundColor Yellow
$serverProcess = Get-Process python -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*manage.py runserver*" }
if ($serverProcess) {
    Write-Host "  Stopping existing server (PID: $($serverProcess.Id))..." -ForegroundColor Yellow
    $serverProcess | Stop-Process -Force
    Start-Sleep -Seconds 2
}

# Run quick test
Write-Host "`n[2] Running quick test..." -ForegroundColor Yellow
& ".\Test-ZamStay.ps1"

# Start server
Write-Host "`n[3] Starting Django server..." -ForegroundColor Yellow
Write-Host "  Server starting on: http://127.0.0.1:8000/" -ForegroundColor White
Write-Host "  Press Ctrl+C to stop the server" -ForegroundColor Gray

# Start server in new window
$serverJob = Start-Job -ScriptBlock {
    Set-Location "C:\Users\Admin\zamreach-project\backend\zamreach"
    python manage.py runserver
}

# Wait a bit and open browser
Start-Sleep -Seconds 3
Write-Host "`n[4] Opening browser..." -ForegroundColor Yellow
Start-Process "http://127.0.0.1:8000/"

Write-Host @"

╔══════════════════════════════════════════════════════════╗
║                  ZAMSTAY IS NOW RUNNING!                 ║
║                                                          ║
║  🌐 Browser opened: http://127.0.0.1:8000/              ║
║                                                          ║
║  To stop: Press Ctrl+C in this window                   ║
║  To test: Run .\Test-ZamStay.ps1                        ║
║  To fix: Run .\Fix-ZamStay.ps1                          ║
╚══════════════════════════════════════════════════════════╝
"@ -ForegroundColor Green

# Keep script running
Write-Host "`nServer is running in background..." -ForegroundColor Gray
Write-Host "Press any key to stop the server and exit" -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# Clean up
Stop-Job $serverJob -Force
Remove-Job $serverJob -Force
Write-Host "`n✅ Server stopped. Goodbye!" -ForegroundColor Green
