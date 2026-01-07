# Upstash Patterns

Redis, QStash, and Rate Limiting patterns for Python backends.

## Redis Client Setup

```python
# Sync client from env
from upstash_redis import Redis
redis = Redis.from_env()

# Async client from env
from upstash_redis.asyncio import Redis
redis = Redis.from_env()

# Explicit credentials
redis = Redis(
    url="UPSTASH_REDIS_REST_URL",
    token="UPSTASH_REDIS_REST_TOKEN"
)
```

---

## Key Expiration (TTL)

```python
import datetime

redis.set("session", "data")
redis.expire("session", 300)  # 5 minutes
redis.expire("token", datetime.timedelta(hours=1))

# Set with inline expiration
redis.set("key", "value", ex=300)  # expires in 300s
redis.setex("key", 300, "value")   # alternative syntax

# Check TTL
ttl = redis.ttl("session")  # seconds remaining
```

---

## Hash Operations

Store structured data:

```python
# Set multiple fields
redis.hset("user:1", values={
    "name": "Alice",
    "email": "alice@example.com",
    "status": "active"
})

# Get single field
name = redis.hget("user:1", "name")

# Get all fields
user = redis.hgetall("user:1")
```

---

## Transactions (Atomic)

```python
tx = redis.multi()
tx.set("account:1", 1000)
tx.decrby("account:1", 100)
tx.set("account:2", 500)
tx.incrby("account:2", 100)
results = tx.exec()  # all or nothing
```

---

## Pipeline (Batch)

Send multiple commands in a single roundtrip:

```python
pipeline = redis.pipeline()
pipeline.set("foo", 1)
pipeline.incr("foo")
pipeline.get("foo")
result = pipeline.exec()
print(result)  # [True, 2, '2']
```

---

## Lists (Queues)

```python
# Push to list
redis.lpush("queue", "task1", "task2")  # Add to head
redis.rpush("queue", "task3")           # Add to tail

# Get range
items = redis.lrange("queue", 0, -1)    # All items
recent = redis.lrange("queue", 0, 9)    # First 10

# Pop items
first = redis.lpop("queue")  # Remove from head

# Recent activity feed (keep last 100)
redis.lpush("user:123:activity", activity_json)
redis.ltrim("user:123:activity", 0, 99)
```

---

## Sets (Unique Values)

```python
redis.sadd("tags:article:1", "python", "redis", "backend")
tags = redis.smembers("tags:article:1")
is_member = redis.sismember("tags:article:1", "python")

# Set operations
common = redis.sinter("user:1:skills", "user:2:skills")
all_skills = redis.sunion("user:1:skills", "user:2:skills")
```

---

## Sorted Sets (Leaderboards)

```python
# Add scores
redis.zadd("leaderboard", {"alice": 100, "bob": 85, "charlie": 92})

# Get top 3 (highest first)
top3 = redis.zrevrange("leaderboard", 0, 2, withscores=True)

# Get rank
rank = redis.zrevrank("leaderboard", "bob")

# Increment score
redis.zincrby("leaderboard", 10, "bob")
```

---

## FastAPI Caching

```python
from fastapi import FastAPI
from upstash_redis import Redis

app = FastAPI()
redis = Redis.from_env()
CACHE_TTL = 600  # 10 minutes

@app.get("/data/{id}")
def get_data(id: str):
    cache_key = f"data:{id}"
    
    # Check cache
    cached = redis.get(cache_key)
    if cached:
        return {"source": "cache", "data": cached}
    
    # Fetch from source
    data = fetch_from_database(id)
    
    # Cache and return
    redis.setex(cache_key, CACHE_TTL, data)
    return {"source": "db", "data": data}
```

---

## FastAPI Session Management

```python
from fastapi import FastAPI, Response, Cookie, HTTPException
from upstash_redis import Redis
import uuid

redis = Redis.from_env()
app = FastAPI()
SESSION_TTL = 900  # 15 minutes

@app.post("/login")
async def login(username: str, response: Response):
    session_id = str(uuid.uuid4())
    redis.hset(f"session:{session_id}", values={
        "user": username, "status": "active"
    })
    redis.expire(f"session:{session_id}", SESSION_TTL)
    response.set_cookie("session_id", session_id, httponly=True)
    return {"message": "Logged in"}

@app.get("/profile")
async def profile(session_id: str = Cookie(None)):
    if not session_id:
        raise HTTPException(403, "No session")
    session = redis.hgetall(f"session:{session_id}")
    if not session:
        raise HTTPException(401, "Session expired")
    redis.expire(f"session:{session_id}", SESSION_TTL)  # sliding
    return session
```

---

## Rate Limiting

### Basic Setup

```python
from upstash_ratelimit import Ratelimit, FixedWindow, SlidingWindow, TokenBucket
from upstash_redis import Redis

redis = Redis.from_env()

# Fixed window: 10 requests per 10 seconds
ratelimit = Ratelimit(
    redis=redis,
    limiter=FixedWindow(max_requests=10, window=10),
)

# Sliding window (smoother)
ratelimit = Ratelimit(
    redis=redis,
    limiter=SlidingWindow(max_requests=10, window=10),
)

# Token bucket (allows bursts)
ratelimit = Ratelimit(
    redis=redis,
    limiter=TokenBucket(max_tokens=10, refill_rate=5, interval=10),
)
```

### FastAPI Rate Limiting

```python
from fastapi import FastAPI, HTTPException, Request

@app.get("/api/resource")
def protected(request: Request):
    result = ratelimit.limit(request.client.host)
    if not result.allowed:
        raise HTTPException(429, "Rate limit exceeded")
    return {"data": "..."}
```

### Multi-Tier Rate Limits

```python
ratelimits = {
    "free": Ratelimit(
        redis=redis,
        limiter=SlidingWindow(max_requests=10, window=60),
        prefix="ratelimit:free"
    ),
    "pro": Ratelimit(
        redis=redis,
        limiter=SlidingWindow(max_requests=100, window=60),
        prefix="ratelimit:pro"
    ),
}
```

### Rate Limit Headers

```python
@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    result = ratelimit.limit(request.client.host)
    
    if not result.allowed:
        return Response(
            content="Rate limit exceeded",
            status_code=429,
            headers={
                "X-RateLimit-Limit": str(result.limit),
                "X-RateLimit-Remaining": "0",
                "Retry-After": str(result.reset)
            }
        )
    
    response = await call_next(request)
    response.headers["X-RateLimit-Limit"] = str(result.limit)
    response.headers["X-RateLimit-Remaining"] = str(result.remaining)
    return response
```

---

## QStash - Background Jobs

### Setup

```python
from qstash import QStash

client = QStash("<QSTASH_TOKEN>")
# Or from env
client = QStash.from_env()
```

### Publish Messages

```python
# Simple publish
res = client.message.publish_json(
    url="https://my-api.com/webhook",
    body={"event": "user_signup", "user_id": 123}
)

# With delay
res = client.message.publish_json(
    url="https://my-api.com/process",
    body={"task": "heavy_computation"},
    delay="5m",
)
```

### Schedule Recurring Jobs

```python
# Daily at midnight
client.schedule.create(
    destination="https://my-api.com/daily-report",
    cron="0 0 * * *"
)

# Every hour
client.schedule.create(
    destination="https://my-api.com/sync",
    cron="0 * * * *"
)
```

### Signature Verification

```python
from qstash import Receiver
from fastapi import FastAPI, Request, HTTPException

receiver = Receiver(
    current_signing_key="...",
    next_signing_key="..."
)

@app.post("/webhook")
async def webhook(request: Request):
    signature = request.headers.get("Upstash-Signature")
    body = await request.body()
    
    try:
        receiver.verify(
            body=body.decode(),
            signature=signature,
            url=str(request.url)
        )
    except Exception:
        raise HTTPException(401, "Invalid signature")
    
    data = await request.json()
    return await process_task(data)
```

### Batch Messages

```python
result = client.message.batch_json([
    {"url": "https://api.com/user/1/notify", "body": {"message": "Hello 1"}},
    {"url": "https://api.com/user/2/notify", "body": {"message": "Hello 2"}},
])
```

---

## Best Practices

1. Use environment variables for credentials
2. Always set TTLs to avoid memory bloat
3. Use key prefixes: `user:123`, `session:abc`, `cache:weather:london`
4. Choose rate limit algorithm based on needs
5. Use async client for async routes
6. Verify QStash signatures for webhook security
7. Use transactions for atomic operations
