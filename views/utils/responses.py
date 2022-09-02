from sanic import json


def _error_http_response(msg, code):
    response = json({
        'success': False,
        'errors': [{'code': code, 'message': msg}] if isinstance(msg, str) else msg
    }, status=code)
    return response


def _http_response(data, code):
    response = json({
        'success': True,
        'data': data,
    }, status=code)
    return response


# SUCCESS http responses

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


# ERROR http responses

def http_not_activated(user_uuid):
    code = 401
    msg = f'Your account is not activated. Please activate your account by following this link: http://127.0.0.1:8000/api/users/activate/{user_uuid}'
    return _error_http_response(msg, code)


def not_found(msg):
    code = 404
    return _error_http_response(msg, code)


def http_forbidden():
    code = 403
    msg = 'You do not have permission to views this page'
    return _error_http_response(msg, code)


def insufficient_funds():
    code = 402
    msg = 'There are not enough funds in your account'
    return _error_http_response(msg, code)
