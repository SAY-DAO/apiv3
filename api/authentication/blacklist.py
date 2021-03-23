from app.services import RedisService


redis = RedisService().redis
TOKEN_KEY = 'BLACKLIST_%s'


def is_token_blacklisted(jti: str):
    return bool(redis.get(TOKEN_KEY % jti))


def blacklist_token(jti: str, ttl: int):
    from pudb import set_trace; set_trace()
    return redis.set(TOKEN_KEY % jti, 1, ttl)
