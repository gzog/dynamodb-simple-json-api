import time


class Cache:
    def __init__(self):
        self.cache = {}

    def set(self, key, value, ttl):
        expire_time = time.time() + ttl
        self.cache[key] = {"value": value, "expire_time": expire_time}

    def get(self, key):
        cur_time = time.time()
        if key in self.cache:
            if self.cache[key]["expire_time"] > cur_time:
                return self.cache[key]["value"]
            else:
                del self.cache[key]
        return None

    def evict_expired(self):
        cur_time = time.time()
        keys_to_evict = [
            key for key, item in self.cache.items() if item["expire_time"] <= cur_time
        ]
        for key in keys_to_evict:
            del self.cache[key]


cache = Cache()
