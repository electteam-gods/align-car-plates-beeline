import redis
from typing import Optional

r: Optional[redis.Redis] = None

def get_redis():
    global r
    if r is None:
        r = redis.Redis(host="redis", port=6379, db=0)
    return r
