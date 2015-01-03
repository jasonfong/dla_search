import pickle

from django.core.cache.backends.memcached import BaseMemcachedCache

class GoogleMemcachedCache(BaseMemcachedCache):
    "An implementation of a cache binding using Google App Engine hosted memcache"
    def __init__(self, server, params):
        from google.appengine.api import memcache
        super(GoogleMemcachedCache, self).__init__(server, params,
                                                   library=memcache,
                                                   value_not_found_exception=ValueError)

    @property
    def _cache(self):
        if getattr(self, '_client', None) is None:
            self._client = self._lib.Client(self._servers, pickleProtocol=pickle.HIGHEST_PROTOCOL)
        return self._client
