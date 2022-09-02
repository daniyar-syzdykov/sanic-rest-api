from sanic.exceptions import SanicException


class IntegrityException(SanicException):
    status_code = 400
    message: str = 'User with this credentials already exists'
    quiet = True
