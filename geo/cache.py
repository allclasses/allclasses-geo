from gevent import monkey
monkey.patch_all()

import memcache
import json

import settings


mc = memcache.Client(settings.MEMCACHE_SERVERS)


def get(request):
    cached = mc.get(request.hash)
    if cached:
        return json.loads(cached)


def save(request, result):
    if isinstance(result, dict):
        return mc.set(request.hash, json.dumps(result))


def clear():
    mc.flush_all()
