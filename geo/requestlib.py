import urlparse
import json
import hashlib


class AbortException(BaseException):
    def __init__(self, status, error):
        self.status = status
        self.error = error


class Request(object):
    """
    Convenience class for storing the important components of
    an incoming network request
    """
    def __init__(self, env):
        self.env = env
        self.authorization = env.get('HTTP_AUTHORIZATION', '')
        self.path = env['PATH_INFO']
        self.method = env['REQUEST_METHOD']
        self.query_string = env['QUERY_STRING']

        self._parameters = None
        self._body = None
        self._hash = None

    @property
    def parameters(self):
        if self._parameters is None:
            self._parameters = urlparse.parse_qs(self.env['QUERY_STRING'])
        return self._parameters

    @property
    def body(self):
        """
        Extracts the request body from the given `env`
        """
        if self._body is None:
            try:
                length = int(self.env.get('CONTENT_LENGTH', '0'))
            except ValueError:
                length = 0
            if length:
                self._body = self.env['wsgi.input'].read(length)
        return self._body or ""

    @property
    def hash(self):
        """
        Generate unique hash of the request for caching
        """
        if self._hash is None:
            self._hash = hashlib.md5(
                self.method + self.path + self.query_string + self.body
            ).hexdigest()
        return self._hash

    def json(self):
        try:
            return json.loads(self.body)
        except ValueError:
            raise AbortException(400, "Request body not valid JSON")
