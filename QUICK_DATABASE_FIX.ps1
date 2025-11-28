# QUICK FIX: Recreate Databases and Restart Services
# This script will:
# 1. Delete old database files
# 2. Provide commands to restart services

Write-Host "=" -ForegroundColor Cyan
Write-Host "  FOOD DELIVERY SYSTEM - DATABASE QUICK FIX" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "🗑️  Step 1: Deleting old database files..." -ForegroundColor Yellow
Write-Host ""

# Delete database files
$databases = @(
    "microservices\order-service\order_service.db",
    "microservices\payment-service\payment_service.db"
)

foreach ($db in $databases) {
    if (Test-Path $db) {
        Remove-Item $db -Force
        Write-Host "Deleted: $db" -ForegroundColor Green
    } else {
        Write-Host " Not found: $db" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "Database files deleted!" -ForegroundColor Green
Write-Host ""
Write-Host "NEXT STEPS:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. STOP all running services (Ctrl+C in each terminal)" -ForegroundColor White
Write-Host ""
Write-Host "2. RESTART services with these commands:" -ForegroundColor White
Write-Host ""
Write-Host "   Terminal 1 - API Gateway:" -ForegroundColor Cyan
Write-Host "   cd microservices\api-gateway" -ForegroundColor Gray
Write-Host "   python app.py" -ForegroundColor Gray
Write-Host ""
Write-Host "   Terminal 2 - User Service:" -ForegroundColor Cyan
Write-Host "   cd microservices\user-service" -ForegroundColor Gray
Write-Host "   python app.py" -ForegroundColor Gray
Write-Host ""
Write-Host "   Terminal 3 - Restaurant Service:" -ForegroundColor Cyan
Write-Host "   cd microservices\restaurant-service" -ForegroundColor Gray
Write-Host "   python app.py" -ForegroundColor Gray
Write-Host ""
Write-Host "   Terminal 4 - Order Service:" -ForegroundColor Cyan
Write-Host "   cd microservices\order-service" -ForegroundColor Gray
Write-Host "   python app.py" -ForegroundColor Gray
Write-Host ""
Write-Host "   Terminal 5 - Delivery Service:" -ForegroundColor Cyan
Write-Host "   cd microservices\delivery-service" -ForegroundColor Gray
Write-Host "   python app.py" -ForegroundColor Gray
Write-Host ""
Write-Host "   Terminal 6 - Payment Service:" -ForegroundColor Cyan
Write-Host "   cd microservices\payment-service" -ForegroundColor Gray
Write-Host "   python app.py" -ForegroundColor Gray
Write-Host ""
Write-Host "3. VERIFY each service prints:" -ForegroundColor White
Write-Host "   [Service] tables created" -ForegroundColor Green
Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "After restart, test with Postman!" -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Cyan
