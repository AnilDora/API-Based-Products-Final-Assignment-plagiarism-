Write-Host "Starting Kong API Gateway with Flask API..."

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "Docker not found. Please install Docker Desktop."
    exit 1
}

Write-Host "Starting services with Docker Compose..."
docker-compose up -d

Write-Host ""
Write-Host "Waiting for services to be ready..."
Start-Sleep -Seconds 10

Write-Host ""
Write-Host "Services started!"
Write-Host "Kong Proxy: http://localhost:8000"
Write-Host "Kong Admin API: http://localhost:8001"
Write-Host "Flask API (direct): http://localhost:5000"
Write-Host ""
Write-Host "Access your API through Kong at: http://localhost:8000"
Write-Host ""
Write-Host "Rate Limiting: 100 requests per minute, 1000 per hour"
Write-Host "Request Size Limit: 10MB"
Write-Host ""
Write-Host "To stop: docker-compose down"
