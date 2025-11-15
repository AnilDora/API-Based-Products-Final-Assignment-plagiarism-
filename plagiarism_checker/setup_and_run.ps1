Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Plagiarism Checker - Setup Script" -ForegroundColor Cyan
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
Write-Host "  Step 2: Preparing Dataset" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

python data_prep.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Failed to prepare dataset" -ForegroundColor Red
    exit 1
}

Write-Host "✓ Dataset prepared successfully" -ForegroundColor Green
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Step 3: Training ML Model" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

python model.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Failed to train model" -ForegroundColor Red
    exit 1
}

Write-Host "✓ Model trained successfully" -ForegroundColor Green
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Step 4: Launching Application" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Starting Streamlit app..." -ForegroundColor Yellow
Write-Host "The app will open in your default browser" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Ctrl+C to stop the application" -ForegroundColor Gray
Write-Host ""

streamlit run app.py
