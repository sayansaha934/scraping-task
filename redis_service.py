from redis import Redis
import ujson

class RedisService:
    def __init__(self) -> None:
        self.redis_client = Redis.from_url(url=f"redis://localhost:6379/10")

    def bulk_insert(self, data, ttl=60):
        with self.redis_client.pipeline() as pipe:
            for key, value in data.items():
                pipe.set(key, ujson.dumps(value))
            pipe.execute()