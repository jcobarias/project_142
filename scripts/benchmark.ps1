# benchmark.ps1 - Benchmarking MSS Implementations
# This script runs the three MSS implementations against different scales of input and reports execution times.

$ErrorActionPreference = "Stop"

# Define Scales
$Scales = @{
    "Small Scale"  = @{ n = 10; k = 3 }
    "Medium Scale" = @{ n = 14; k = 3 }
    "Large Scale"  = @{ n = 16; k = 3 }
}

# Implementation Executables
$Implementations = @{
    "Brute Force"       = ".\brute_force.exe"
    "L-Assignment"      = ".\l_assignment.exe"
    "L-Star Assignment" = ".\l_star_ass.exe"
}

# Function to generate random input
function Get-RandomInput($n, $k) {
    $elements = 1..$n | ForEach-Object { Get-Random -Minimum 1 -Maximum 100 }
    return "$n`n$($elements -join ' ')`n$k"
}

# Ensure executables exist
foreach ($exe in $Implementations.Values) {
    if (-not (Test-Path $exe)) {
        Write-Error "Executable $exe not found. Please compile the C files first."
    }
}

$Results = @()

Write-Host "Starting Benchmarks..." -ForegroundColor Cyan

foreach ($scaleName in "Small Scale", "Medium Scale", "Large Scale") {
    $params = $Scales[$scaleName]
    $n = $params.n
    $k = $params.k
    
    Write-Host "Testing $scaleName (n=$n, k=$k)..." -ForegroundColor Yellow
    
    $inputData = Get-RandomInput $n $k
    
    $row = [PSCustomObject]@{
        Scale = $scaleName
    }
    
    foreach ($implName in "Brute Force", "L-Assignment", "L-Star Assignment") {
        $exe = $Implementations[$implName]
        
        Write-Host "  Running $implName..." -NoNewline
        
        try {
            $rawOutput = $inputData | & $exe
            $outputStr = $rawOutput -join "`n"
            if ($outputStr -match "Execution time: ([\d.]+) seconds") {
                $time = [double]$Matches[1]
                $row | Add-Member -MemberType NoteProperty -Name $implName -Value ("{0:N6}s" -f $time)
                Write-Host " Done ($time s)" -ForegroundColor Green
            } else {
                $row | Add-Member -MemberType NoteProperty -Name $implName -Value "Error"
                Write-Host " Failed to parse output" -ForegroundColor Red
            }
        } catch {
            $row | Add-Member -MemberType NoteProperty -Name $implName -Value "Timeout/Error"
            Write-Host " Error running executable: $($_.Exception.Message)" -ForegroundColor Red
        }
    }
    $Results += $row
}

Write-Host "`n--- Execution Time Matrix ---" -ForegroundColor Cyan
$Results | Format-Table -AutoSize
