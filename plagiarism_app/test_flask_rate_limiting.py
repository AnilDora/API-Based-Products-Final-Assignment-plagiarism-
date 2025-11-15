import requests
import time

BASE_URL = "http://localhost:5001"

def test_token_bucket():
    print("\nTesting Token Bucket Endpoint")
    print("=" * 60)
    print("Making 12 rapid requests (limit is 10)")
    print("-" * 60)
    
    success = 0
    limited = 0
    
    for i in range(1, 13):
        try:
            res = requests.get(f"{BASE_URL}/token-bucket", timeout=2)
            
            if res.status_code == 200:
                success += 1
                print(f"Request {i}: SUCCESS (200)")
            elif res.status_code == 429:
                limited += 1
                data = res.json()
                print(f"Request {i}: RATE LIMITED (429) - {data['message']}")
        except Exception as e:
            print(f"Request {i}: ERROR - {e}")
        
        time.sleep(0.1)
    
    print()
    print(f"Results: {success} successful, {limited} rate limited")
    print()
    print("Waiting 3 seconds for token refill...")
    time.sleep(3)
    
    print("Making 5 more requests after refill:")
    for i in range(13, 18):
        try:
            res = requests.get(f"{BASE_URL}/token-bucket", timeout=2)
            
            if res.status_code == 200:
                print(f"Request {i}: SUCCESS (200)")
            elif res.status_code == 429:
                data = res.json()
                print(f"Request {i}: RATE LIMITED (429)")
        except Exception as e:
            print(f"Request {i}: ERROR - {e}")
        
        time.sleep(0.1)

def test_leaky_bucket():
    print("\n\nTesting Leaky Bucket Endpoint")
    print("=" * 60)
    print("Making 8 rapid requests (capacity is 5)")
    print("-" * 60)
    
    success = 0
    limited = 0
    
    for i in range(1, 9):
        try:
            res = requests.get(f"{BASE_URL}/leaky-bucket", timeout=2)
            
            if res.status_code == 200:
                success += 1
                print(f"Request {i}: ADDED TO QUEUE (200)")
            elif res.status_code == 429:
                limited += 1
                data = res.json()
                print(f"Request {i}: REJECTED (429) - {data['message']}")
        except Exception as e:
            print(f"Request {i}: ERROR - {e}")
        
        time.sleep(0.1)
    
    print()
    print(f"Results: {success} added to queue, {limited} rejected")
    print()
    print("Waiting 3 seconds for bucket to leak...")
    time.sleep(3)
    
    print("Making 3 more requests after leak:")
    for i in range(9, 12):
        try:
            res = requests.get(f"{BASE_URL}/leaky-bucket", timeout=2)
            
            if res.status_code == 200:
                print(f"Request {i}: ADDED TO QUEUE (200)")
            elif res.status_code == 429:
                data = res.json()
                print(f"Request {i}: REJECTED (429)")
        except Exception as e:
            print(f"Request {i}: ERROR - {e}")
        
        time.sleep(0.1)

if __name__ == "__main__":
    print("\nRate Limiting Algorithms - Flask Integration Test")
    print("=" * 60)
    print("Make sure flask_rate_limiting_demo.py is running on port 5001")
    print("=" * 60)
    
    try:
        res = requests.get(f"{BASE_URL}/", timeout=2)
        if res.status_code == 200:
            print("API is running!")
            
            test_token_bucket()
            test_leaky_bucket()
            
            print("\n\n" + "=" * 60)
            print("Tests completed!")
            print("=" * 60)
        else:
            print(f"API returned unexpected status: {res.status_code}")
    except Exception as e:
        print(f"ERROR: Cannot connect to API at {BASE_URL}")
        print(f"Please start the Flask server first:")
        print("  python flask_rate_limiting_demo.py")
