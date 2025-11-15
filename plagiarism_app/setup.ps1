Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Plagiarism App - Setup Script" -ForegroundColor Cyan
Write-Host "  (Flask API + Streamlit)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found. Please install Python 3.7+" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Step 1: Installing Dependencies" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Failed to install dependencies" -ForegroundColor Red
    exit 1
}

Write-Host "✓ Dependencies installed successfully" -ForegroundColor Green
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Step 2: Training ML Model" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

Set-Location flask_api
python model.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Failed to train model" -ForegroundColor Red
    Set-Location ..
    exit 1
}

Set-Location ..
Write-Host "✓ Model trained successfully" -ForegroundColor Green
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "To run the application, you need TWO terminals:" -ForegroundColor Yellow
Write-Host ""
Write-Host "Terminal 1 (Flask API):" -ForegroundColor Cyan
Write-Host "  cd flask_api" -ForegroundColor White
Write-Host "  python app.py" -ForegroundColor White
Write-Host ""
Write-Host "Terminal 2 (Streamlit Frontend):" -ForegroundColor Cyan
Write-Host "  cd streamlit_app" -ForegroundColor White
Write-Host "  streamlit run app.py" -ForegroundColor White
Write-Host ""
Write-Host "Or use the provided run scripts:" -ForegroundColor Yellow
Write-Host "  .\run_api.ps1     (in Terminal 1)" -ForegroundColor White
Write-Host "  .\run_frontend.ps1 (in Terminal 2)" -ForegroundColor White
Write-Host ""
