import json
import os
import redis


class CacheService:
    def __init__(self):
        host = os.getenv("REDIS_HOST", "localhost")
        port = int(os.getenv("REDIS_PORT", 6379))
        db = int(os.getenv("REDIS_DB", 0))
        
        self.client = redis.Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=True
        )

    def get(self, key: str):
        value = self.client.get(key)
        if value: 
            return json.loads(value)
        return None
    
    def set(self, key: str, value, expire_seconds: int = 3600):
        self.client.set(key, json.dumps(value), ex=expire_seconds)

    def ping(self) -> bool:
        try:
            return self.client.ping()
        except Exception:
            return False