import requests

KONG_URL = "http://localhost:8000/check"

print("Request Size Limiting Demo")
print("=" * 50)
print("Kong limit: 10MB maximum request size")
print("=" * 50)
print()

small_text = "This is a small test file." * 100
large_text = "X" * (11 * 1024 * 1024)

print("Test 1: Small file (should work)")
print("-" * 50)
try:
    res = requests.post(KONG_URL, files={
        "original": ("orig.txt", small_text.encode()),
        "submission": ("sub.txt", small_text.encode())
    }, timeout=5)
    
    if res.status_code == 200:
        print("Status: 200 OK - Request accepted")
    else:
        print(f"Status: {res.status_code}")
except Exception as e:
    print(f"Error: {e}")

print()
print("Test 2: Large file - 11MB (should be blocked)")
print("-" * 50)
try:
    res = requests.post(KONG_URL, files={
        "original": ("orig.txt", large_text.encode()),
        "submission": ("sub.txt", large_text.encode())
    }, timeout=5)
    
    if res.status_code == 413:
        print("Status: 413 Request Entity Too Large")
        print("Request blocked by Kong - Size limit working!")
    elif res.status_code == 200:
        print("Status: 200 OK - Request accepted (limit not working)")
    else:
        print(f"Status: {res.status_code}")
except Exception as e:
    print(f"Error: {e}")

print()
print("=" * 50)
print("Demo complete")
print("=" * 50)
