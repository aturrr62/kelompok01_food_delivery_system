#!/usr/bin/env powershell
<#
.SYNOPSIS
Food Delivery System - Comprehensive Service Starter
Jalankan API Gateway + 5 Microservices dalam tab terpisah

.DESCRIPTION
Script ini membuka 6 terminal baru untuk:
- Port 5000: API Gateway 
- Port 5001: User Service 👤 (ARTHUR)
- Port 5002: Restaurant Service 🍽️ (rizki)
- Port 5003: Order Service (Nadia)
- Port 5004: Delivery Service 🚚 (aydin)
- Port 5005: Payment Service 💳 (reza)

.EXAMPLE
.\START_ALL_SERVICES.ps1
#>

$ErrorActionPreference = "Continue"
$project_root = Get-Location

Write-Host "
╔═══════════════════════════════════════════════════════════════╗
║   FOOD DELIVERY SYSTEM - COMPREHENSIVE STARTUP               ║
║                                                               ║
║   Launching: API Gateway + 5 Microservices                   ║
╚═══════════════════════════════════════════════════════════════╝
" -ForegroundColor Cyan

# Define services
$services = @(
    @{
        name = "API Gateway"
        port = 5000
        path = "microservices/api-gateway"
        description = "API Gateway (Main Entry Point)"
        color = "Cyan"
    },
    @{
        name = "User Service"
        port = 5001
        path = "microservices/user-service"
        description = "User Management (ARTHUR)"
        color = "Green"
    },
    @{
        name = "Restaurant Service"
        port = 5002
        path = "microservices/restaurant-service"
        description = "Restaurant Management (rizki)"
        color = "Yellow"
    },
    @{
        name = "Order Service"
        port = 5003
        path = "microservices/order-service"
        description = "Order Management (Nadia)"
        color = "Magenta"
    },
    @{
        name = "Delivery Service"
        port = 5004
        path = "microservices/delivery-service"
        description = "Delivery Management (aydin)"
        color = "Red"
    },
    @{
        name = "Payment Service"
        port = 5005
        path = "microservices/payment-service"
        description = "Payment Management (reza)"
        color = "Blue"
    }
)

# Function to create startup script for each service
function Create-ServiceScript {
    param(
        [string]$ServiceName,
        [int]$Port,
        [string]$ServicePath,
        [string]$Description
    )
    
    $script_content = @"
# Service: $ServiceName on port $Port
# Description: $Description

Set-Location "$project_root"
Write-Host "
╔════════════════════════════════════════════════════════════════╗
║  Starting: $ServiceName                                    
║  Port: $Port
║  Path: $ServicePath
║  $Description
╚════════════════════════════════════════════════════════════════╝
" -ForegroundColor Green

# Install dependencies
Write-Host "Installing dependencies for $ServiceName..." -ForegroundColor Yellow
Set-Location "$project_root\$ServicePath"
python -m pip install -r requirements.txt -q

# Start service
Write-Host "Starting service on port $Port..." -ForegroundColor Cyan
python app.py

# If script exits, show error
Write-Host "Service $ServiceName stopped unexpectedly!" -ForegroundColor Red
Read-Host "Press Enter to close..."
"@
    
    return $script_content
}

# Create temporary scripts directory
$temp_scripts_dir = "$project_root\.service_scripts"
if (-not (Test-Path $temp_scripts_dir)) {
    New-Item -ItemType Directory -Path $temp_scripts_dir -Force | Out-Null
}

Write-Host "Creating service startup scripts..." -ForegroundColor Yellow

# Create and launch each service in new PowerShell window
$count = 0
foreach ($service in $services) {
    $count++
    
    $script_file = "$temp_scripts_dir\start_$($service.port).ps1"
    $script_content = Create-ServiceScript -ServiceName $service.name -Port $service.port -ServicePath $service.path -Description $service.description
    
    Set-Content -Path $script_file -Value $script_content
    
    Write-Host "  [$count/6] Creating script for $($service.name)" -ForegroundColor White
    
    # Open new PowerShell window with the script
    Start-Process powershell -ArgumentList "-NoExit", "-File", $script_file -WindowStyle Normal
    
    # Small delay to avoid overwhelming the system
    Start-Sleep -Milliseconds 500
}

Write-Host "
╔════════════════════════════════════════════════════════════════╗
║  All services launched! 6 new PowerShell windows opened.      ║
║                                                                ║
║  Service URLs:                                                ║
║     • API Gateway (Main):  http://localhost:5000              ║
║     • User Service:         http://localhost:5001             ║
║     • Restaurant Service:   http://localhost:5002             ║
║     • Order Service:        http://localhost:5003             ║
║     • Delivery Service:     http://localhost:5004             ║
║     • Payment Service:      http://localhost:5005             ║
║                                                                ║
║  Health Check:                                                ║
║     GET http://localhost:5000/health                          ║
║                                                                ║
║  Swagger/API Docs:                                            ║
║     GET http://localhost:5000/api/docs                        ║
║                                                                ║
║  Wait 15-20 seconds for all services to start, then test!    ║
║                                                                ║
║  Run test script (after all services start):                 ║
║     python docs/test_api.py                                   ║
║                                                                ║
║  Tip: Keep all 6 terminal windows visible to monitor          ║
║     errors and startup progress!                              ║
╚════════════════════════════════════════════════════════════════╝
" -ForegroundColor Green

Write-Host "
✋ This launcher window will stay open. You can close it anytime.
   Services will continue running in their own windows.

Press Enter to close this launcher...
" -ForegroundColor Yellow

Read-Host
