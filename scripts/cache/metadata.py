from dataclasses import dataclass
from datetime import datetime


@dataclass
class CacheMetadata:
    """
    Metadata describing one cache entry.
    """

    created_at: datetime
    expires_at: datetime
    key: str
    version: int = 1