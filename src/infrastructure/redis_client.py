import redis.asyncio as redis
from src.config import get_settings
_redis_pool = None

async def init_redis() -> None:
    global _redis_pool
    settings = get_settings()
    _redis_pool = redis.ConnectionPool.from_url(settings.REDIS_URL, decode_responses=False)

async def close_redis() -> None:
    if _redis_pool:
        await _redis_pool.disconnect()

async def get_redis() -> redis.Redis:
    if _redis_pool is None:
        raise RuntimeError('Redis not initialized')
    return redis.Redis(connection_pool=_redis_pool)