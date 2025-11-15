from flask import Flask, request, jsonify
from functools import wraps
import time
import threading

app = Flask(__name__)

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
    
    def add_request(self, request_id=None):
        with self.lock:
            self.leak()
            
            if len(self.queue) < self.capacity:
                self.queue.append(request_id or time.time())
                return True
            return False

token_bucket = TokenBucket(capacity=10, refill_rate=2)
leaky_bucket = LeakyBucket(capacity=5, leak_rate=1)

def token_bucket_limiter(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not token_bucket.consume(1):
            return jsonify({
                "error": "Rate limit exceeded (Token Bucket)",
                "message": "Too many requests. Please wait and try again."
            }), 429
        return f(*args, **kwargs)
    return decorated

def leaky_bucket_limiter(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not leaky_bucket.add_request():
            return jsonify({
                "error": "Rate limit exceeded (Leaky Bucket)",
                "message": "Queue is full. Please wait and try again."
            }), 429
        return f(*args, **kwargs)
    return decorated

@app.route("/")
def home():
    return jsonify({
        "message": "Rate Limiting Algorithms Demo",
        "endpoints": {
            "/token-bucket": "Protected by Token Bucket (10 tokens, refill 2/sec)",
            "/leaky-bucket": "Protected by Leaky Bucket (5 capacity, leak 1/sec)",
            "/unlimited": "No rate limiting"
        }
    })

@app.route("/token-bucket")
@token_bucket_limiter
def token_bucket_endpoint():
    return jsonify({
        "message": "Success! Request processed.",
        "algorithm": "Token Bucket",
        "timestamp": time.time()
    })

@app.route("/leaky-bucket")
@leaky_bucket_limiter
def leaky_bucket_endpoint():
    return jsonify({
        "message": "Success! Request added to queue.",
        "algorithm": "Leaky Bucket",
        "timestamp": time.time()
    })

@app.route("/unlimited")
def unlimited_endpoint():
    return jsonify({
        "message": "Success! No rate limiting.",
        "timestamp": time.time()
    })

if __name__ == "__main__":
    print("Rate Limiting Flask API")
    print("=" * 50)
    print("Token Bucket: /token-bucket (10 tokens, refill 2/sec)")
    print("Leaky Bucket: /leaky-bucket (5 capacity, leak 1/sec)")
    print("=" * 50)
    app.run(debug=True, host="0.0.0.0", port=5001)
