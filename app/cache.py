# app/cache.py
import aioredis
import json
from typing import Optional, Dict

redis = None

async def init_cache(redis_url: str = "redis://localhost") -> aioredis.Redis:
    global redis
    redis = await aioredis.create_redis_pool(redis_url)
    return redis

async def close_cache() -> None:
    global redis
    if redis:
        redis.close()
        await redis.wait_closed()

async def get_cached_data(key: str) -> Optional[Dict]:
    if not redis:
        return None
    data = await redis.get(key)
    if data:
        return json.loads(data)
    return None

async def set_cached_data(key: str, value: Dict, expire: int = 60) -> None:
    if not redis:
        return
    await redis.set(key, json.dumps(value), expire=expire)
