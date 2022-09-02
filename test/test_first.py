import json
import random
import pytest
from sanic import Sanic, response
import database as db
from database.schemas import *
from .conftest import sanic_app


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
async def test_auth_without_payload():
    request, response = await sanic_app.asgi_client.post('/auth')
    assert request.method.lower() == 'post'
    assert response.json['reasons'][0] == 'Authorization header not present.'
    assert response.status == 400


@pytest.mark.asyncio
async def test_verify_jwt_with_no_token():
    request, response = await sanic_app.asgi_client.get('/auth/verify')
    response_json = json.loads(response.body)

    assert request.method.lower() == 'get'
    assert response_json['exception'] == 'MissingAuthorizationHeader'
    assert response.status == 401


@pytest.mark.asyncio
async def test_registring_new_user():
    username = 'testuser1'
    password = 'testpass1'

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
async def test_get_jwt_tokens():
    user = CACHE.get('user', None)
    request, response = await sanic_app.asgi_client.post('/auth', headers=HEADERS, json={'username': user['username'], 'password': user['password']})
    response_json = json.loads(response.body)
    # print('response json is -----------------> ', response_json)    
    # print(response_json['access_token'])

    assert request.method.lower() == 'post'
    assert user is not None
    assert response_json['access_token'] != ''
    assert response_json['refresh_token'] != ''

    CACHE.update({'access_token': response_json['access_token']})
    CACHE.update({'refresh_token': response_json['refresh_token']})



@pytest.mark.asyncio
async def test_valid_jwt_access_tokens():
    access_token = CACHE.get('access_token', None)
    HEADERS.update({'Authorization': 'Bearer ' + access_token})
    request, response = await sanic_app.asgi_client.get('/auth/verify', headers=HEADERS)
    response_json = json.loads(response.body)

    assert request.method.lower() == 'get'
    assert access_token is not None
    assert response_json['valid'] is True


@pytest.mark.asyncio
async def test_auth_with_invalid_token():
    headers = {
		'Accept': '*/*',
		'Accept-Encoding': 'gzip, deflate, br',
		'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjpudWxsLCJleHAiOjE2NjE2OTQ3NTV9.Ys8F5GhUv45qfavNriRpyml73Jym-wxCU83D8vLm2RU',
		'Content-Length': '57',
		'Content-Type': 'application/json',
		'Host': 'httpbin.org',
		'User-Agent': 'PostmanRuntime/7.29.2',
		'X-Amzn-Trace-Id': 'Root=1-6310be89-06518def47f6b54d6b98a339'
	}
    request, response = await sanic_app.asgi_client.get('/auth/verify', headers=headers)

    response_json = json.loads(response.body)

    assert request.method.lower() == 'get'
    assert response_json['exception'] == 'InvalidToken'
    assert response.status == 401
