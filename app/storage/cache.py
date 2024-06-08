from cachetools import TTLCache


class UserLocation:
    def __init__(self):
        self.cache = TTLCache(maxsize=1000, ttl=3600)

    def getLocation(self, userId: str) -> tuple[float, float]:
        item = self.cache.get(userId)
        return item

    def setLocation(self, userId: str, latitude: float, longitude: float):
        self.cache[userId] = (latitude, longitude)
