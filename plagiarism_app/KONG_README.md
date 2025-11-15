# Kong API Gateway Setup

This folder contains Kong API Gateway configuration with rate limiting and request size limiting.

## What is Kong?

Kong is an API Gateway that sits between clients and your Flask API. It provides:
- Rate limiting (controls how many requests per user)
- Request size limiting (blocks large requests)
- Authentication and security
- Monitoring and logging

## Files

docker-compose.yml - Runs Kong, PostgreSQL database, and Flask API in Docker
kong.yml - Kong configuration with plugins
start_kong.ps1 - Start everything
stop_kong.ps1 - Stop everything

## Setup

1. Install Docker Desktop for Windows
2. Run: .\start_kong.ps1
3. Wait for services to start (10-15 seconds)
4. Access API through Kong at http://localhost:8000

## Kong Plugins Configured

Rate Limiting:
- 100 requests per minute
- 1000 requests per hour
- Returns 429 error when exceeded

Request Size Limiting:
- Maximum 10MB per request
- Returns 413 error if exceeded

## URLs

Kong Proxy: http://localhost:8000 (use this for API calls)
Kong Admin: http://localhost:8001 (admin interface)
Flask API: http://localhost:5000 (direct access, bypasses Kong)

## Testing Rate Limiting

Try making more than 100 requests in a minute - Kong will return error 429.

## Stopping

Run: .\stop_kong.ps1
Or: docker-compose down
