'''
封装memcache缓存模块
'''
import memcache

cache = memcache.Client(['118.25.48.34:11211'], debug=True)


def set(key, value, timeout=60):
    '''
    设置键值对
    '''
    return cache.set(key, value, timeout)


def get(key):
    return cache.get(key)


def delete(key):
    return cache.delete(key)
