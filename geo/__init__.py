#!/usr/bin/env python
from gevent import monkey
monkey.patch_all()

import gevent
import json
import itsdangerous

from requestlib import Request, AbortException
import services
import cache
import settings


signer = itsdangerous.Signer(settings.SECRET_KEY)


def application(env, start_response):
    request = Request(env)

    try:
        _validate(request)
        status, result = _process(request)
    except AbortException as e:
        status, result = e.status, {"error": e.error}

    response = json.dumps(result)
    headers = [
        ("Content-Type", "application/json"),
        ("Content-Length", str(len(response)))
    ]

    start_response(str(status), headers)
    return response


def _process(request):
    # Try cache for response
    cached = cache.get(request)
    if cached is not None:
        return 202, {"result": cached}

    # Get data and service
    data = request.json()
    service = services.registry[request.path]()

    # Generate a response
    result = service.get(data)

    # Cache the result with a spawned event and return response
    gevent.spawn(cache.save, request, result)
    return 202, {"result": result}


def _validate(request):
    # Check auth header
    try:
        assert request.authorization
        assert signer.unsign(request.authorization)
    except (AssertionError, itsdangerous.BadSignature):
        raise AbortException(403, "Authorization required")

    # Check method
    if request.method != 'POST':
        raise AbortException(405, "Methods supported: POST")

    # Check service path is known
    if request.path not in services.registry:
        raise AbortException(404, "Service not found")
