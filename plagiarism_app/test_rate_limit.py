import requests
import time

KONG_URL = "http://localhost:8000/health"

print("Rate Limiting Demo")
print("=" * 50)
print("Kong limits: 100 requests per minute")
print("=" * 50)
print()

print("Making 105 rapid requests to Kong Gateway...")
print("-" * 50)

success = 0
rate_limited = 0
errors = 0

for i in range(1, 106):
    try:
        res = requests.get(KONG_URL, timeout=5)
        
        if res.status_code == 200:
            success += 1
            if i <= 5 or i % 20 == 0:
                print(f"Request {i}: Success (200)")
        elif res.status_code == 429:
            rate_limited += 1
            print(f"Request {i}: RATE LIMITED (429) - Too many requests!")
            remaining = res.headers.get('X-RateLimit-Remaining-Minute', 'N/A')
            limit = res.headers.get('X-RateLimit-Limit-Minute', 'N/A')
            print(f"  -> Rate limit exceeded. Limit: {limit}/minute")
        else:
            errors += 1
            print(f"Request {i}: Error {res.status_code}")
    except Exception as e:
        errors += 1
        if i <= 5:
            print(f"Request {i}: Connection error - {e}")

print()
print("=" * 50)
print("Results:")
print(f"Successful requests: {success}")
print(f"Rate limited (429): {rate_limited}")
print(f"Other errors: {errors}")
print("=" * 50)
print()

if rate_limited > 0:
    print("SUCCESS: Rate limiting is working!")
    print(f"Kong blocked {rate_limited} requests after the limit was reached.")
else:
    print("INFO: All {success} requests succeeded.")
    print("To see rate limiting, make more than 100 requests per minute.")
