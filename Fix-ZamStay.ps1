# ZamStay Quick Fix - Run if something breaks
Write-Host "ZamStay Quick Fix Script" -ForegroundColor Cyan
Write-Host "="*50 -ForegroundColor Cyan

# 1. Fix template encoding
Write-Host "`n[1] Fixing template encoding..." -ForegroundColor Yellow

function Repair-Template {
    param($path)
    if (Test-Path $path) {
        $content = Get-Content $path -Raw
        $content = $content -replace '\x95', '-'
        $content = $content -replace '\x91', "'"
        $content = $content -replace '\x92', "'"
        $content = $content -replace '\x93', '"'
        $content = $content -replace '\x94', '"'
        $utf8 = New-Object System.Text.UTF8Encoding $false
        [System.IO.File]::WriteAllText($path, $content, $utf8)
        Write-Host "  ✅ Fixed: $path" -ForegroundColor Green
    }
}

Repair-Template "templates\customer\home.html"
Repair-Template "templates\customer\search.html"

# 2. Clear Python cache
Write-Host "`n[2] Clearing Python cache..." -ForegroundColor Yellow
Remove-Item -Path "__pycache__" -Recurse -ErrorAction SilentlyContinue
Remove-Item -Path "bookings\__pycache__" -Recurse -ErrorAction SilentlyContinue
Remove-Item -Path "zamreach\__pycache__" -Recurse -ErrorAction SilentlyContinue
Write-Host "  ✅ Cleared Python cache" -ForegroundColor Green

# 3. Check Django
Write-Host "`n[3] Testing Django..." -ForegroundColor Yellow
try {
    python manage.py check
    Write-Host "  ✅ Django check passed" -ForegroundColor Green
} catch {
    Write-Host "  ❌ Django check failed" -ForegroundColor Red
}

Write-Host "`n" + "="*50 -ForegroundColor Cyan
Write-Host "✅ QUICK FIX COMPLETE!" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor White
Write-Host "1. Restart server: python manage.py runserver" -ForegroundColor Yellow
Write-Host "2. Test: .\Test-ZamStay.ps1" -ForegroundColor Yellow
Write-Host "3. Visit: http://127.0.0.1:8000/" -ForegroundColor Yellow
