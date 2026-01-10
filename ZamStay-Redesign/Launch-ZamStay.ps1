# ZamStay Redesign Launcher
Write-Host "Starting ZamStay Property Listing Redesign..." -ForegroundColor Green
Write-Host "Opening in default browser..." -ForegroundColor Cyan

# Open the HTML file in default browser
Start-Process "index.html"

Write-Host "App should now be running in your browser." -ForegroundColor Green
Write-Host "Files available in: $(Get-Location)" -ForegroundColor Yellow
