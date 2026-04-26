import redis.asyncio as redis
from src.config import Config

JTI_EXPIRY = 3600

jwt_blocklist = redis.Redis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    db=0,
    decode_responses=True,  # important for returning strings instead of bytes
)


async def add_jti_to_blocklist(jti: str) -> None:
    await jwt_blocklist.set(
        name=jti,
        value="",
        ex=JTI_EXPIRY,
    )


async def token_in_blocklist(jti: str) -> bool:
    value = await jwt_blocklist.get(jti)
    return value is not None
