import json
import pytest
from sanic import Sanic, response
import database as db
from database.schemas import *
from .conftest import sanic_app, random_user_credantials


Sanic.test_mode = True

CACHE = {}
HEADERS = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Length': '57',
    'Content-Type': 'application/json',
    'Host': 'httpbin.org',
    'User-Agent': 'PostmanRuntime/7.29.2',
    'X-Amzn-Trace-Id': 'Root=1-6310be89-06518def47f6b54d6b98a339'
}


@pytest.mark.asyncio
async def test_registring_new_user():
    username, password = random_user_credantials()

    request, response = await sanic_app.asgi_client.post('/api/users', headers=HEADERS, json={'username': username, 'password': password})
    db_user = await db.User.get_by_username(username)
    user = user_schema.dump(db_user)
    response_json = json.loads(response.body)

    assert request.method.lower() == 'post'
    assert user != {}
    assert response_json['success'] is True
    assert user['is_active'] is False
    assert user['bills'] != []
    assert user['bills'][0]['transactions'] != []

    user.update({'password': password})
    CACHE.update({'user': user})


@pytest.mark.asyncio
async def test_activate_user():
    user = CACHE.get('user', None)
    user_uuid = user['uuid']
    request, response = await sanic_app.asgi_client.patch(f'/api/users/activate/{user_uuid}')
    response_json = json.loads(response.body)

    db_user = await db.User.get_by_username(user['username'])
    _user = user_schema.dump(db_user)

    assert request.method.lower() == 'patch'
    assert _user['is_active'] is True


@pytest.mark.asyncio
async def test_get_all_users():
    request, response = await sanic_app.asgi_client.get('/api/users', headers=HEADERS)
    response_json = json.loads(response.body)

    assert request.method.lower() == 'get'
    assert len(response_json) != 0


@pytest.mark.asyncio
async def test_get_all_users_without_permission():
    request, response = await sanic_app.asgi_client.get('/api/users', headers=HEADERS)
    response_json = json.loads(response.body)

    assert request.method.lower() == 'get'
    assert len(response_json) != 0
