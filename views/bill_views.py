import database as db
from database.schemas import bill_schema
from sanic import json, Request
from sanic.exceptions import BadRequest


async def create_bill(requset: Request):
    user_id = requset.json.get('user_id', None)
    if user_id is None:
        return BadRequest('pls provide correct user id')
    reslut = await db.Bill.create(user_id=user_id)


async def delet_bill(requset, id):
    await db.Bill.delete(id)
    return True


async def get_bill_by_id(requset, id):
    result = await db.Bill.get_bill_by_id(id)
    ret = bill_schema.dump(result)
    return json(ret)


async def get_all_bills(request):
    result = await db.Bill.get_all_bills()
    ret = bill_schema.dump(result)
    return json(ret)
