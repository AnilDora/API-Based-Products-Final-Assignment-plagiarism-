import time
import threading

class TokenBucket:
    def __init__(self, capacity, refill_rate):
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate
        self.last_refill = time.time()
        self.lock = threading.Lock()
    
    def refill(self):
        now = time.time()
        elapsed = now - self.last_refill
        tokens_to_add = elapsed * self.refill_rate
        self.tokens = min(self.capacity, self.tokens + tokens_to_add)
        self.last_refill = now
    
    def consume(self, tokens=1):
        with self.lock:
            self.refill()
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False
    
    def get_available_tokens(self):
        with self.lock:
            self.refill()
            return self.tokens


class LeakyBucket:
    def __init__(self, capacity, leak_rate):
        self.capacity = capacity
        self.queue = []
        self.leak_rate = leak_rate
        self.last_leak = time.time()
        self.lock = threading.Lock()
    
    def leak(self):
        now = time.time()
        elapsed = now - self.last_leak
        leaks = int(elapsed * self.leak_rate)
        
        if leaks > 0:
            self.queue = self.queue[leaks:]
            self.last_leak = now
    
    def add_request(self, request=None):
        with self.lock:
            self.leak()
            
            if len(self.queue) < self.capacity:
                self.queue.append(request or time.time())
                return True
            return False
    
    def get_queue_size(self):
        with self.lock:
            self.leak()
            return len(self.queue)


def demo_token_bucket():
    print("Token Bucket Algorithm Demo")
    print("=" * 60)
    print("Capacity: 10 tokens")
    print("Refill Rate: 2 tokens per second")
    print("=" * 60)
    print()
    
    bucket = TokenBucket(capacity=10, refill_rate=2)
    
    print("Test 1: Making 10 requests immediately (should all succeed)")
    for i in range(1, 11):
        result = bucket.consume(1)
        status = "ALLOWED" if result else "DENIED"
        print(f"Request {i}: {status} (Tokens left: {bucket.get_available_tokens():.2f})")
    
    print()
    print("Test 2: Making 5 more requests (should be denied - no tokens)")
    for i in range(11, 16):
        result = bucket.consume(1)
        status = "ALLOWED" if result else "DENIED"
        print(f"Request {i}: {status} (Tokens left: {bucket.get_available_tokens():.2f})")
    
    print()
    print("Test 3: Wait 3 seconds for refill (expect 6 tokens)")
    time.sleep(3)
    print(f"After 3 seconds, available tokens: {bucket.get_available_tokens():.2f}")
    
    print()
    print("Test 4: Making 6 requests (should succeed)")
    for i in range(16, 22):
        result = bucket.consume(1)
        status = "ALLOWED" if result else "DENIED"
        print(f"Request {i}: {status} (Tokens left: {bucket.get_available_tokens():.2f})")
    
    print()
    print("=" * 60)


def demo_leaky_bucket():
    print("\n\nLeaky Bucket Algorithm Demo")
    print("=" * 60)
    print("Capacity: 5 requests")
    print("Leak Rate: 1 request per second")
    print("=" * 60)
    print()
    
    bucket = LeakyBucket(capacity=5, leak_rate=1)
    
    print("Test 1: Adding 5 requests immediately (bucket full)")
    for i in range(1, 6):
        result = bucket.add_request()
        status = "ADDED" if result else "REJECTED"
        print(f"Request {i}: {status} (Queue size: {bucket.get_queue_size()})")
    
    print()
    print("Test 2: Adding 3 more requests (should be rejected - bucket full)")
    for i in range(6, 9):
        result = bucket.add_request()
        status = "ADDED" if result else "REJECTED"
        print(f"Request {i}: {status} (Queue size: {bucket.get_queue_size()})")
    
    print()
    print("Test 3: Wait 2 seconds for leak (expect 2 requests leaked)")
    time.sleep(2)
    print(f"After 2 seconds, queue size: {bucket.get_queue_size()}")
    
    print()
    print("Test 4: Adding 2 requests (should succeed)")
    for i in range(9, 11):
        result = bucket.add_request()
        status = "ADDED" if result else "REJECTED"
        print(f"Request {i}: {status} (Queue size: {bucket.get_queue_size()})")
    
    print()
    print("=" * 60)


if __name__ == "__main__":
    demo_token_bucket()
    demo_leaky_bucket()
    
    print("\n\nKey Differences:")
    print("-" * 60)
    print("Token Bucket:")
    print("  - Allows burst traffic up to capacity")
    print("  - Tokens refill continuously")
    print("  - Good for APIs with varying load")
    print()
    print("Leaky Bucket:")
    print("  - Smooths out burst traffic")
    print("  - Processes requests at constant rate")
    print("  - Good for bandwidth limiting")
    print("-" * 60)
