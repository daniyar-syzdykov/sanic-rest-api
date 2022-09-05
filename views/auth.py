import jwt
import uuid
import database as db
from sanic import Sanic
from sanic.request import Request
from sanic_jwt import exceptions as jwt_exceptions, BaseEndpoint, Responses
from sanic_jwt.endpoints import RefreshEndpoint
from database.schemas import user_auth_schema
from sanic.exceptions import *


async def authenticate(request: Request):
    if not request.json:
        raise jwt_exceptions.MissingAuthorizationHeader()
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    user: db.User = await db.User.get_by_username(username)
    if not user:
        raise NotFound('User not found')

    user_json = user_auth_schema.dump(user)
    user_json['user_id'] = user_json['id']

    if not username or not password:
        raise jwt_exceptions.AuthenticationFailed('User not found.')

    if password != user.password:
        raise jwt_exceptions.AuthenticationFailed('Invalid password.')

    return user_json


async def store_token(request, user_id, refresh_token):
    print('store refresh token was called')
    await db.User.update(user_id, refresh_token=refresh_token)


async def retrive_refresh_token(request, user_id, *args, **kwargs):
    result = await db.User.get_refresh_tokens(user_id)
    return result


async def generate_refresh_token():
    return uuid.uuid4().hex


async def retrieve_user(request: Request, payload, *args, **kwargs):
    if payload:
        user_id = payload.get('user_id', None)
        user = await db.User.get_user_by_id(user_id)
        user_json = user_auth_schema.dump(user)
        user_json['user_id'] = user_json['id']
        return user_json
    return None


class CustomResponses(Responses):
    @staticmethod
    async def extend_refresh(request, user=None, access_token=None, refresh_token=None, purported_token=None, payload=None):
        user_access_token = await db.User.get_access_token(user['user_id'])
        user_refresh_token = await db.User.get_refresh_tokens(user['user_id'])
        print(user_access_token, access_token)
        if user_refresh_token == refresh_token:
            new_refresh_token = uuid.uuid4().hex
            await db.User.update(user['user_id'], access_token=access_token)
            await db.User.update(user['user_id'], refresh_token=new_refresh_token)
            return {"refresh_token": new_refresh_token}
        raise jwt_exceptions.AuthenticationFailed('This refresh token has been expired')
