import os
from abc import abstractmethod


class RemoteCacheBackend:
    """
    A backend implementation for accessing a remote/distributed cache.
    """

    def __init__(self, cache_id: str):
        pass

    @abstractmethod
    def get(self, key: str):
        pass

    @abstractmethod
    def put(self, key: str, data: bytes):
        pass


class RedisRemoteCacheBackend(RemoteCacheBackend):
    """
    A Redis implementation of a remote/distributed cache.
    """

    def __init__(self, cache_id: str):
        import redis

        self._cache_id = cache_id
        self._key_fmt = os.environ.get(
            "TORCHINDUCTOR_REDIS_KEY_FORMAT", "inductor:{cache_id}:{key}"
        )
        self._redis = redis.Redis(
            host=os.environ.get("TRITON_REDIS_HOST", "localhost"),
            port=int(os.environ.get("TRITON_REDIS_PORT", 6379)),
        )

    def _get_key(self, key: str) -> str:
        return self._key_fmt.format(cache_id=self._cache_id, key=key)

    def get(self, key: str):
        return self._redis.get(self._get_key(key))

    def put(self, key: str, data: bytes):
        return self._redis.set(self._get_key(key), data)
