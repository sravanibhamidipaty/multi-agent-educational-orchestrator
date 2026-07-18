import hashlib, json, redis
from config import REDIS_URL

_redis = redis.Redis.from_url(REDIS_URL, decode_responses=True)


def _key(namespace: str, *parts) -> str:
    raw = "|".join(str(p) for p in parts)
    return f"{namespace}:{hashlib.sha1(raw.encode()).hexdigest()}"

def cached_json(namespace: str, ttl: int, compute, *key_parts):
    key = _key(namespace, *key_parts)
    hit = _redis.get(key)
    if hit is not None:
        return json.loads(hit)
    val = compute()
    _redis.setex(key, ttl, json.dumps(val))
    return val