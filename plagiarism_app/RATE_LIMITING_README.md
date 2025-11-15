# Rate Limiting Algorithms Implementation

Implementation of Token Bucket and Leaky Bucket rate limiting algorithms in Python.

## Files

1. rate_limiting_algorithms.py - Core algorithm implementations with demos
2. flask_rate_limiting_demo.py - Flask API with rate limiting decorators
3. test_flask_rate_limiting.py - Test script for Flask endpoints

## Algorithms Implemented

### 1. Token Bucket Algorithm

How it works:
- Bucket has capacity of N tokens
- Tokens refill at rate R per second
- Each request consumes 1 token
- Request allowed if tokens available
- Allows burst traffic up to capacity

Example:
- Capacity: 10 tokens
- Refill rate: 2 tokens/second
- Can handle 10 requests immediately
- After that, 2 requests per second

Use cases:
- API rate limiting with burst allowance
- Download bandwidth management
- Database query throttling

### 2. Leaky Bucket Algorithm

How it works:
- Bucket has capacity of N requests
- Requests leak out at rate R per second
- New requests added to queue
- Request rejected if bucket full
- Smooths out burst traffic

Example:
- Capacity: 5 requests
- Leak rate: 1 request/second
- Can queue up to 5 requests
- Processes 1 request per second

Use cases:
- Traffic shaping
- Network bandwidth limiting
- Queue management

## Running the Demos

### Basic Demo (Console):

python rate_limiting_algorithms.py

Shows both algorithms with test scenarios.

### Flask API Demo:

Terminal 1 - Start server:
python flask_rate_limiting_demo.py

Terminal 2 - Run tests:
python test_flask_rate_limiting.py

### Endpoints:

GET / - API information
GET /token-bucket - Protected by Token Bucket (10 tokens, refill 2/sec)
GET /leaky-bucket - Protected by Leaky Bucket (5 capacity, leak 1/sec)
GET /unlimited - No rate limiting

## Key Differences

Token Bucket vs Leaky Bucket:

Token Bucket:
- Allows burst traffic
- Variable output rate
- Tokens accumulate when idle
- Good for: APIs, downloads, flexible rate limiting

Leaky Bucket:
- Smooths burst traffic
- Constant output rate
- No accumulation when idle
- Good for: Network traffic, bandwidth control, constant rate processing

## Implementation Details

Both classes are thread-safe using threading.Lock().

Token Bucket refills continuously based on elapsed time.
Leaky Bucket processes requests at fixed intervals.

Rate limit response: 429 Too Many Requests

## Configuration

Token Bucket:
capacity - maximum tokens in bucket
refill_rate - tokens added per second

Leaky Bucket:
capacity - maximum queue size
leak_rate - requests processed per second

## Testing Results

Token Bucket:
- 10 requests: All succeed
- Next 5 requests: All denied
- Wait 3 seconds: 6 tokens refilled
- Next 6 requests: All succeed

Leaky Bucket:
- 5 requests: All queued
- Next 3 requests: All rejected
- Wait 2 seconds: 2 requests leaked
- Next 2 requests: Both queued

Both algorithms working as expected.
