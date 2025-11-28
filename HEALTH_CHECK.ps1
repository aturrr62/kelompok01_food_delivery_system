#!/usr/bin/env powershell
<#
.SYNOPSIS
Food Delivery System - Comprehensive Health Check & Troubleshooting
Diagnose issues dengan services

.DESCRIPTION
Script ini melakukan:
1. Port availability check
2. Service connectivity test
3. Database file validation
4. Dependencies verification
5. Process monitoring

.EXAMPLE
.\HEALTH_CHECK.ps1
.\HEALTH_CHECK.ps1 -Mode detailed
.\HEALTH_CHECK.ps1 -Mode cleanup
#>

param(
    [string]$Mode = "quick"  # quick, detailed, cleanup, monitor
)

$ErrorActionPreference = "Continue"

# ============================================================================
# COLORS & FORMATTING
# ============================================================================

function Write-Header {
    param([string]$Text)
    Write-Host "`n╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║ $Text" -ForegroundColor Cyan
    Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
}

function Write-Section {
    param([string]$Text)
    Write-Host "`n─── $Text " -ForegroundColor Yellow -NoNewline
    Write-Host "─" * (60 - $Text.Length) -ForegroundColor Yellow
}

function Write-Success {
    param([string]$Text)
    Write-Host "$Text" -ForegroundColor Green
}

function Write-Error {
    param([string]$Text)
    Write-Host "$Text" -ForegroundColor Red
}

function Write-Warning {
    param([string]$Text)
    Write-Host " $Text" -ForegroundColor Yellow
}

function Write-Info {
    param([string]$Text)
    Write-Host "ℹ️  $Text" -ForegroundColor Cyan
}

# ============================================================================
# PORT & SERVICE CHECKS
# ============================================================================

function Check-Ports {
    Write-Section "🔌 CHECKING PORTS"
    
    $ports = @{
        5000 = "API Gateway "
        5001 = "User Service 👤"
        5002 = "Restaurant Service 🍽️"
        5003 = "Order Service "
        5004 = "Delivery Service 🚚"
        5005 = "Payment Service 💳"
    }
    
    $results = @()
    
    foreach ($port in $ports.Keys) {
        $service_name = $ports[$port]
        
        try {
            $connection = Test-NetConnection -ComputerName localhost -Port $port -WarningAction SilentlyContinue
            
            if ($connection.TcpTestSucceeded) {
                Write-Success "Port $port ($service_name) - LISTENING"
                $results += @{port=$port; service=$service_name; status="OK"}
            } else {
                Write-Warning "Port $port ($service_name) - NOT LISTENING"
                $results += @{port=$port; service=$service_name; status="DOWN"}
            }
        }
        catch {
            Write-Warning "Port $port ($service_name) - CHECK FAILED"
            $results += @{port=$port; service=$service_name; status="ERROR"}
        }
    }
    
    return $results
}

function Check-Health-Endpoints {
    Write-Section "🏥 CHECKING HEALTH ENDPOINTS"
    
    $endpoints = @(
        @{
            url = "http://localhost:5000/health"
            name = "API Gateway"
        },
        @{
            url = "http://localhost:5001/health"
            name = "User Service"
        },
        @{
            url = "http://localhost:5002/health"
            name = "Restaurant Service"
        },
        @{
            url = "http://localhost:5003/health"
            name = "Order Service"
        },
        @{
            url = "http://localhost:5004/health"
            name = "Delivery Service"
        },
        @{
            url = "http://localhost:5005/health"
            name = "Payment Service"
        }
    )
    
    foreach ($endpoint in $endpoints) {
        try {
            $response = Invoke-WebRequest -Uri $endpoint.url -TimeoutSec 5 -ErrorAction Stop
            if ($response.StatusCode -eq 200) {
                Write-Success "$($endpoint.name) - HEALTHY (200)"
            } else {
                Write-Warning "$($endpoint.name) - Status $($response.StatusCode)"
            }
        }
        catch [System.Net.Http.HttpRequestException] {
            Write-Error "$($endpoint.name) - Connection refused"
        }
        catch [System.Net.WebException] {
            Write-Error "$($endpoint.name) - Not responding"
        }
        catch {
            Write-Error "$($endpoint.name) - Error: $($_.Exception.Message)"
        }
    }
}

function Check-Processes {
    Write-Section " CHECKING RUNNING PROCESSES"
    
    $python_processes = Get-Process python -ErrorAction SilentlyContinue
    
    if ($python_processes) {
        Write-Success "Found $($python_processes.Count) Python process(es)"
        foreach ($proc in $python_processes) {
            Write-Info "  • Process ID: $($proc.Id) | Memory: $([math]::Round($proc.WorkingSet/1MB,2))MB"
        }
    } else {
        Write-Error "No Python processes running!"
    }
}

function Check-Databases {
    Write-Section "CHECKING DATABASE FILES"
    
    $db_files = Get-ChildItem -Path "microservices" -Filter "*.db" -Recurse -ErrorAction SilentlyContinue
    
    if ($db_files) {
        Write-Success "Found $($db_files.Count) database file(s)"
        foreach ($db in $db_files) {
            $size_mb = [math]::Round($db.Length/1MB, 2)
            Write-Info "  • $($db.Name) ($size_mb MB) - Last modified: $($db.LastWriteTime)"
        }
    } else {
        Write-Warning "No database files found (might be OK on first run)"
    }
}

function Check-Dependencies {
    Write-Section "CHECKING PYTHON DEPENDENCIES"
    
    $services = @(
        "microservices/api-gateway",
        "microservices/user-service",
        "microservices/restaurant-service",
        "microservices/order-service",
        "microservices/delivery-service",
        "microservices/payment-service"
    )
    
    foreach ($service in $services) {
        $req_file = "$service/requirements.txt"
        
        if (Test-Path $req_file) {
            Write-Success "✓ $service/requirements.txt exists"
        } else {
            Write-Error "✗ $service/requirements.txt MISSING!"
        }
    }
}

# ============================================================================
# CLEANUP FUNCTIONS
# ============================================================================

function Cleanup-Databases {
    Write-Section "🧹 CLEANING UP DATABASE FILES"
    
    Write-Warning "This will delete ALL database files!"
    $confirm = Read-Host "Continue? (y/n)"
    
    if ($confirm -eq 'y') {
        try {
            Remove-Item "microservices/*/*.db" -Force -ErrorAction Stop
            Remove-Item "microservices/*/instance/*.db" -Force -ErrorAction Stop
            Write-Success "Database files cleaned up"
        }
        catch {
            Write-Error "Error during cleanup: $_"
        }
    }
}

function Kill-All-Python {
    Write-Section "🔪 KILLING ALL PYTHON PROCESSES"
    
    Write-Warning "This will kill ALL Python processes!"
    $confirm = Read-Host "Continue? (y/n)"
    
    if ($confirm -eq 'y') {
        try {
            Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force
            Write-Success "All Python processes killed"
            Start-Sleep 2
        }
        catch {
            Write-Error "Error killing processes: $_"
        }
    }
}

function Clean-Cache {
    Write-Section "🗑️  CLEANING PIP CACHE"
    
    try {
        Write-Info "Clearing pip cache..."
        pip cache purge
        Write-Success "Pip cache cleared"
    }
    catch {
        Write-Error "Error clearing cache: $_"
    }
}

# ============================================================================
# MONITORING FUNCTIONS
# ============================================================================

function Monitor-Services {
    Write-Header "MONITORING SERVICES (Press Ctrl+C to stop)"
    
    $iteration = 0
    
    while ($true) {
        Clear-Host
        Write-Header "SERVICE MONITORING - Iteration $iteration"
        
        Write-Info "Timestamp: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
        Write-Info "Refresh every 5 seconds (Press Ctrl+C to stop)`n"
        
        Check-Ports | ForEach-Object {
            if ($_.status -eq "OK") {
                Write-Success "$($_.port) - $($_.service)"
            } else {
                Write-Error "$($_.port) - $($_.service)"
            }
        }
        
        Write-Section "PYTHON PROCESSES"
        $procs = Get-Process python -ErrorAction SilentlyContinue
        if ($procs) {
            Write-Success "$($procs.Count) Python process(es) running"
        } else {
            Write-Error "No Python processes running"
        }
        
        Write-Section "MEMORY USAGE"
        $total_memory = ($procs | Measure-Object -Property WorkingSet -Sum).Sum
        $total_memory_mb = [math]::Round($total_memory/1MB, 2)
        Write-Info "Total Python memory: $total_memory_mb MB"
        
        $iteration++
        Start-Sleep 5
    }
}

# ============================================================================
# MAIN EXECUTION
# ============================================================================

Write-Header "🏥 FOOD DELIVERY SYSTEM - HEALTH CHECK"

switch ($Mode.ToLower()) {
    "quick" {
        Write-Info "Running QUICK health check..."
        Check-Ports
        Check-Processes
        Check-Databases
    }
    
    "detailed" {
        Write-Info "Running DETAILED health check..."
        Check-Ports
        Check-Health-Endpoints
        Check-Processes
        Check-Databases
        Check-Dependencies
    }
    
    "cleanup" {
        Write-Warning "CLEANUP MODE - Destructive operations!"
        Write-Host ""
        Cleanup-Databases
        Kill-All-Python
        Clean-Cache
    }
    
    "monitor" {
        Monitor-Services
    }
    
    default {
        Write-Error "Unknown mode: $Mode"
        Write-Info "Valid modes: quick, detailed, cleanup, monitor"
        exit 1
    }
}

Write-Host ""
Write-Host "Health check complete!" -ForegroundColor Green
Write-Host ""

# Additional recommendations
Write-Section "RECOMMENDATIONS"

$port_results = Check-Ports
$down_ports = $port_results | Where-Object { $_.status -ne "OK" }

if ($down_ports) {
    Write-Warning "Some services are not running:"
    foreach ($down in $down_ports) {
        Write-Info "  • Port $($down.port): $($down.service) - Start it with START_ALL_SERVICES.ps1"
    }
} else {
    Write-Success "All services are running!"
    Write-Info "  • Run TEST_ALL_APIS.py to verify all endpoints"
    Write-Info "  • Run .\HEALTH_CHECK.ps1 -Mode monitor to monitor services"
}

Read-Host "`nPress Enter to exit"
