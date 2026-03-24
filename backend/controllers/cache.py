from flask_caching import Cache
import os

cache = Cache()

def init_cache(app):
    redis_url = os.getenv("REDIS_URL")
    print("Initializing cache with Redis URL:", redis_url)
    app.config["CACHE_TYPE"] = "RedisCache"
    app.config["CACHE_REDIS_URL"] = redis_url  # from Render
    app.config["CACHE_DEFAULT_TIMEOUT"] = 300

    cache.init_app(app)