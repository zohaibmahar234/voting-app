# Start backend server
$backendJob = Start-Job -ScriptBlock {
    Set-Location "d:\project\vonting-app\vonting-app\voting-backend"
    mvn spring-boot:run
}

# Wait for backend to start
Start-Sleep -Seconds 10

# Start frontend server
$frontendJob = Start-Job -ScriptBlock {
    Set-Location "d:\project\vonting-app\vonting-app\voting-frontend"
    python app.py
}

Write-Host "Starting servers..."
Write-Host "Backend will be available at: http://localhost:8080"
Write-Host "Frontend will be available at: http://127.0.0.1:5000"

try {
    # Keep script running and showing output
    while ($true) {
        Receive-Job -Job $backendJob
        Receive-Job -Job $frontendJob
        Start-Sleep -Seconds 1
    }
} finally {
    # Cleanup on script termination
    Stop-Job -Job $backendJob
    Stop-Job -Job $frontendJob
    Remove-Job -Job $backendJob
    Remove-Job -Job $frontendJob
}
