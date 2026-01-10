# ZamStay Permanent Test - Run after server restart
Write-Host "Testing ZamStay Setup..." -ForegroundColor Cyan

# Check essential files
$essentialFiles = @(
    "templates\customer\home.html",
    "templates\customer\search.html", 
    "bookings\views.py",
    "bookings\urls.py"
)

Write-Host "`n[1] Checking essential files..." -ForegroundColor Yellow
$allExist = $true
foreach ($file in $essentialFiles) {
    if (Test-Path $file) {
        $size = "{0:N0}" -f ((Get-Item $file).Length / 1KB)
        Write-Host "  ✅ $file ($size KB)" -ForegroundColor Green
    } else {
        Write-Host "  ❌ Missing: $file" -ForegroundColor Red
        $allExist = $false
    }
}

# Test Django setup
Write-Host "`n[2] Testing Django..." -ForegroundColor Yellow
try {
    $djangoTest = python -c "
import django
django.setup()
from django.template.loader import get_template
try:
    get_template('customer/home.html')
    print('✅ Homepage template loads')
except Exception as e:
    print(f'❌ Template error: {e}')
" 2>&1
    
    if ($djangoTest -match "✅") {
        Write-Host "  $djangoTest" -ForegroundColor Green
    } else {
        Write-Host "  $djangoTest" -ForegroundColor Red
        $allExist = $false
    }
} catch {
    Write-Host "  ❌ Django test failed: $_" -ForegroundColor Red
    $allExist = $false
}

# Test URLs
Write-Host "`n[3] Testing server response..." -ForegroundColor Yellow
$serverRunning = $false
try {
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:8000/" -TimeoutSec 2 -ErrorAction SilentlyContinue
    if ($response.StatusCode -eq 200) {
        Write-Host "  ✅ Server is running" -ForegroundColor Green
        $serverRunning = $true
    }
} catch {
    Write-Host "  ⚠️  Server not running (expected if not started)" -ForegroundColor Yellow
}

Write-Host "`n" + "="*50 -ForegroundColor Cyan
if ($allExist) {
    Write-Host "✅ ALL CHECKS PASSED!" -ForegroundColor Green
    Write-Host "Your ZamStay is ready to go!" -ForegroundColor White
    Write-Host "`n🌐 Visit: http://127.0.0.1:8000/" -ForegroundColor Yellow
} else {
    Write-Host "⚠️  SOME CHECKS FAILED" -ForegroundColor Red
    Write-Host "Check the errors above and run the fix script again." -ForegroundColor White
}

if (-not $serverRunning) {
    Write-Host "`n🚀 Start server with: python manage.py runserver" -ForegroundColor Cyan
}
