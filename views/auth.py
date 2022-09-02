from sanic.request import Request
import database as db
from sanic_jwt import exceptions as jwt_exceptions
from database.schemas import user_schema
from sanic.exceptions import *

async def authenticate(request: Request):
    if not request.json:
        raise jwt_exceptions.MissingAuthorizationHeader()
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    user: db.User = await db.User.get_by_username(username)
    if not user:
        raise NotFound('User not found')

    user_json = user_schema.dump(user)
    user_json['user_id'] = user_json['id']
    print('user_json ----------> ', user_json)
    print(user.password)

    if not username or not password:
        raise jwt_exceptions.AuthenticationFailed('User not found.')

    if password != user.password:
        raise jwt_exceptions.AuthenticationFailed('Invalid password.')

    return user_json


async def store_token(request, user_id, refresh_token):
    await db.User.update(user_id, refresh_token=refresh_token)


async def get_token(request, user_id, refresh_token):
    result = await db.User.get_refresh_token(user_id)
    print(result)

async def retrieve_user(request: Request, payload, *args, **kwargs):
    print(payload)
    if payload:
        user_id = payload.get('user_id', None)
        user = await db.User.get_user_by_id(user_id)
        user_json = user_schema.dump(user)
        return user_json

    return None
