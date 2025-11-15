Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Starting Streamlit Frontend" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "⚠ Make sure Flask API is running first!" -ForegroundColor Yellow
Write-Host "   Run 'run_api.ps1' in another terminal" -ForegroundColor Yellow
Write-Host ""

Write-Host "Starting Streamlit on http://localhost:8501" -ForegroundColor Green
Write-Host "The app will open in your default browser" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to stop the application" -ForegroundColor Gray
Write-Host ""

Set-Location streamlit_app
streamlit run app.py
