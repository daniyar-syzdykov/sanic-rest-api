from sanic import json
from sanic.exceptions import SanicException, BadRequest
from sanic import HTTPResponse
from sanic import json


def _http_response(data, code):
    response = json({
        'success': True,
        'data': data,
    }, status=code)
    return response

def http_created(data):
    code = 201
    return _http_response(data, code)


def http_empty():
    code = 204
    return _http_response(data='', code=code)


def purchase_completed():
    code = 200
    msg = 'Purchase completed'
    return _http_response(msg, code)
