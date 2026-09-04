from datetime import datetime, timedelta
from pathlib import Path

from scripts.cache.serializer import CacheSerializer
from scripts.utils.logger import logger


class CacheManager:
    """
    Manages cached JSON payloads.
    Each cache entry is stored as:
        cache/<key>.json
    """

    def __init__(self, cache_directory="cache", expiration_hours=12,):
        self.cache_directory = Path(cache_directory)
        self.expiration = timedelta(hours=expiration_hours)

    # --------------------------------------------------

    def cache_path(self, key,):
        return self.cache_directory / f"{key}.json"

    # --------------------------------------------------

    def exists(self, key,):
        return self.cache_path(key).exists()

    # --------------------------------------------------

    def expired(self, key,):

        path = self.cache_path(key)
        if not path.exists():
            return True

        modified = datetime.fromtimestamp(path.stat().st_mtime)
        age = datetime.now() - modified
        return age > self.expiration

    # --------------------------------------------------

    def load(self, key,):

        logger.info(f"Loading cache: {key}")
        return CacheSerializer.load(
            self.cache_path(key)
        )

    # --------------------------------------------------

    def save(self, key, payload,):
        logger.info(f"Saving cache: {key}")
        CacheSerializer.save(
            self.cache_path(key),
            payload,
        )

    # --------------------------------------------------

    def invalidate(self, key,):
        path = self.cache_path(key)
        if path.exists():
            logger.info(f"Removing cache: {key}")
            path.unlink()

    # --------------------------------------------------

    def get_or_fetch(self, key, fetch,):

        """
        Return cached payload.
        Otherwise execute the supplied
        fetch() function.
        """

        if (
            self.exists(key)
            and
            not self.expired(key)
        ):
            return self.load(key)

        logger.info(f"Cache miss: {key}")
        payload = fetch()
        self.save(key, payload,)
        return payload