Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Starting Flask API Server" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if (-not (Test-Path "flask_api\plagiarism_model.pkl")) {
    Write-Host "⚠ Model file not found!" -ForegroundColor Yellow
    Write-Host "Running model training first..." -ForegroundColor Yellow
    Write-Host ""
    
    Set-Location flask_api
    python model.py
    Set-Location ..
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "✗ Failed to train model" -ForegroundColor Red
        exit 1
    }
    Write-Host ""
}

Write-Host "Starting Flask API on http://localhost:5000" -ForegroundColor Green
Write-Host ""
Write-Host "API Endpoints:" -ForegroundColor Yellow
Write-Host "  GET  /         - API information" -ForegroundColor White
Write-Host "  GET  /health   - Health check" -ForegroundColor White
Write-Host "  POST /check    - Check plagiarism" -ForegroundColor White
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Gray
Write-Host ""

Set-Location flask_api
python app.py
