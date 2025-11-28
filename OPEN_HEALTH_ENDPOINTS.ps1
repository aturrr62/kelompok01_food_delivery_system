# Quick Screenshot Helper Script
# This script will open all health endpoints in browser tabs

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   FOOD DELIVERY SYSTEM" -ForegroundColor Yellow
Write-Host "   Screenshot Helper Script" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Create evidence directory if not exists
$evidencePath = "c:\xampp\htdocs\food_delivery_system\evidence"
if (-not (Test-Path $evidencePath)) {
    New-Item -ItemType Directory -Force -Path $evidencePath | Out-Null
    Write-Host "Created evidence directory: $evidencePath" -ForegroundColor Green
} else {
    Write-Host "Evidence directory exists: $evidencePath" -ForegroundColor Green
}

Write-Host ""
Write-Host "Checking if services are running..." -ForegroundColor Yellow
Write-Host ""

# Function to check if port is listening
function Test-Port {
    param([int]$Port)
    $connection = Test-NetConnection -ComputerName localhost -Port $Port -WarningAction SilentlyContinue -ErrorAction SilentlyContinue
    return $connection.TcpTestSucceeded
}

# Check all services
$services = @(
    @{Name="API Gateway"; Port=5000; HealthUrl="http://localhost:5000/health"; ScreenshotName="health-gateway.png"},
    @{Name="User Service"; Port=5001; HealthUrl="http://localhost:5001/health"; ScreenshotName="health-user.png"},
    @{Name="Restaurant Service"; Port=5002; HealthUrl="http://localhost:5002/health"; ScreenshotName="health-restaurant.png"},
    @{Name="Order Service"; Port=5003; HealthUrl="http://localhost:5003/health"; ScreenshotName="health-order.png"},
    @{Name="Delivery Service"; Port=5004; HealthUrl="http://localhost:5004/health"; ScreenshotName="health-delivery.png"},
    @{Name="Payment Service"; Port=5005; HealthUrl="http://localhost:5005/health"; ScreenshotName="health-payment.png"}
)

$allRunning = $true

foreach ($service in $services) {
    $isRunning = Test-Port -Port $service.Port
    if ($isRunning) {
        Write-Host "$($service.Name) is running on port $($service.Port)" -ForegroundColor Green
    } else {
        Write-Host "$($service.Name) is NOT running on port $($service.Port)" -ForegroundColor Red
        $allRunning = $false
    }
}

Write-Host ""

if (-not $allRunning) {
    Write-Host " WARNING: Not all services are running!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please start all services first:" -ForegroundColor Yellow
    Write-Host "  1. cd microservices\api-gateway && python app.py" -ForegroundColor Gray
    Write-Host "  2. cd microservices\user-service && python app.py" -ForegroundColor Gray
    Write-Host "  3. cd microservices\restaurant-service && python app.py" -ForegroundColor Gray
    Write-Host "  4. cd microservices\order-service && python app.py" -ForegroundColor Gray
    Write-Host "  5. cd microservices\delivery-service && python app.py" -ForegroundColor Gray
    Write-Host "  6. cd microservices\payment-service && python app.py" -ForegroundColor Gray
    Write-Host ""
    $continue = Read-Host "Do you want to continue anyway? (y/n)"
    if ($continue -ne "y") {
        Write-Host "Aborted." -ForegroundColor Red
        exit
    }
}

Write-Host ""
Write-Host "Opening health endpoints in browser..." -ForegroundColor Yellow
Write-Host ""

foreach ($service in $services) {
    Write-Host "  Opening: $($service.HealthUrl)" -ForegroundColor Cyan
    Start-Process $service.HealthUrl
    Start-Sleep -Seconds 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   INSTRUCTIONS" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "TAKE SCREENSHOTS NOW!" -ForegroundColor Green
Write-Host ""
Write-Host "For each browser tab:" -ForegroundColor White
Write-Host "  1. Press [Windows + Shift + S] to take screenshot" -ForegroundColor Gray
Write-Host "  2. Select the area containing the JSON response" -ForegroundColor Gray
Write-Host "  3. Open Paint or image editor" -ForegroundColor Gray
Write-Host "  4. Press [Ctrl + V] to paste" -ForegroundColor Gray
Write-Host "  5. Save to: $evidencePath\[filename].png" -ForegroundColor Gray
Write-Host ""
Write-Host "Screenshot filenames:" -ForegroundColor White
foreach ($service in $services) {
    Write-Host "  - $($service.ScreenshotName)" -ForegroundColor Cyan
}
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   ALTERNATIVE METHOD (Windows 11)" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Press [Windows + Shift + S]" -ForegroundColor Gray
Write-Host "2. Screenshot will be saved to clipboard" -ForegroundColor Gray
Write-Host "3. Click notification to open Snipping Tool" -ForegroundColor Gray
Write-Host "4. Click [Save] and choose location" -ForegroundColor Gray
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   NEXT STEPS" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "After taking health screenshots:" -ForegroundColor White
Write-Host "  1. Take Swagger UI screenshots" -ForegroundColor Cyan
Write-Host "     - http://localhost:5000/api-docs/" -ForegroundColor Gray
Write-Host "  2. Take Postman screenshots" -ForegroundColor Cyan
Write-Host "     - Import collection & environment" -ForegroundColor Gray
Write-Host "     - Run collection" -ForegroundColor Gray
Write-Host "  3. Create video demo (see VIDEO_DEMO_GUIDE.md)" -ForegroundColor Cyan
Write-Host "  4. Update video/link.txt with YouTube/Drive URL" -ForegroundColor Cyan
Write-Host ""
Write-Host "See detailed guide: TAKE_SCREENSHOTS_GUIDE.md" -ForegroundColor Yellow
Write-Host ""
Write-Host "Script completed successfully!" -ForegroundColor Green
Write-Host ""
