from sanic.request import Request
from sanic.response import json
import database as db
from database.schemas import product_schema
from sanic_jwt import protected, inject_user
from .utils import *
from sanic.exceptions import *


@inject_user()
@protected()
async def create_product(request: Request, user=None):
    if not user['is_admin']:
        return json({'success': False, 'message': 'you do not have permission'})

    data = request.json
    result = await db.Product.create(name=data['name'], description=data['description'], price=data['price'])
    ret = product_schema.dump(result)
    return json(ret)


async def get_product_by_id(request: Request, id):
    result = await db.Product.get_by_id(id)

    if not result:
        raise NotFound('Product not found')

    ret = product_schema.dump(result)
    return json(ret)


async def get_all_products(request: Request):
    result = await db.Product.get_all()

    if not result:
        raise NotFound('Product not found')

    ret = product_schema.dump(result, many=True)
    return json(ret)


def find_bill(bills: list[db.Bill], target_bill: int) -> db.Bill | None:
    for bill in range(len(bills)):
        if bills[bill]['id'] == target_bill:
            return bills[bill]
    return None


@inject_user()
@protected()
async def buy_product(request: Request, user: db.User, product_id):
    if not user['is_active']:
        return http_not_activated(user['uuid'])

    bill_id = request.json.get('bill_id', None)
    if not bill_id:
        return json({'success': False, 'message': 'no bill provided'})

    bill = find_bill(user['bills'], bill_id)
    if not bill:
        return json({'success': False, 'message': f'Your do not have bill: {bill_id}'})

    product: db.Product = await db.Product.get_by_id(product_id)
    if bill['balance'] < product.price:
        return insufficient_funds()
    await db.Bill.update(bill_id, balance=bill['balance'] - product.price)
    return purchase_completed()


@inject_user()
@protected()
async def delete_product(request: Request, user, id):
    if not user['is_admin']:
        return json({'success': False, 'message': 'you do not have permission'})
    result = await db.Product.delete(id)
    ret = product_schema.dump(result)
    return json(ret)
