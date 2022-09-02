import database as db
from sanic import json, Request
from sanic.exceptions import BadRequest, Forbidden
from database.schemas import user_schema, user_register_schema
from sanic_jwt import protected, inject_user
from .utils import *
from sanic.exceptions import *


# @inject_user()
# @protected()
async def get_all_users(request, user: db.User = None):
    # if not user['is_admin'] or not user['is_active']:
    #     raise Forbidden('You do not have permission to views this page')
    #     # return json({'success': False, 'message': 'you do not have permission'})

    result = await db.User.get_all_users()
    if not result:
        raise NotFound('There is not users in database')

    ret = user_schema.dump(result, many=True)
    return json(ret)


@inject_user()
@protected()
async def get_user_by_id(requset, user_id, user: db.User=None):
    if user['id'] == user_id and not user['is_active']:
        return http_not_activated(user['uuid'])

    if user['id'] != user_id and user['is_admin'] == False:
        return http_forbidden()

    result: db.User = await db.User.get_user_by_id(user_id)
    if not result:
        raise NotFound('User not found')

    ret = user_schema.dump(result)
    return json(ret)


async def create_user(request: Request):
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if username is None or password is None:
        raise BadRequest('Pls provide valid credantials')
    result = await db.User.create(username=username, password=password)

    user_id = result['id']
    bill_result = await db.Bill.create(user_id=user_id, balance=10000000)

    bill_id = bill_result['id']
    await db.Transaction.create(bill_id=bill_id)

    user_uuid = result['uuid']
    
    return http_created({'activation_link': f'http://127.0.0.1:8000/api/users/activate/{user_uuid}'})


async def activate_user(requset, uuid):
    await db.User.activate_user(uuid)
    return json({'success': True})


@inject_user()
@protected()
async def delete_user(requset, user, id):
    if not user['is_admin']:
        raise Forbidden('You do not have permission to views this page')
    reslut = await db.User.delete(id)
    return True
