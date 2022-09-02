import database as db
from database.schemas import transaction_schema
from sanic import json, Request
from sanic.exceptions import BadRequest


async def create_transaction(request: Request):
    bill_id = request.json.get('bill_id', None)
    amount = request.json.get('amount', None)

    if bill_id is None or amount is None:
        raise BadRequest('pls provide bill id and amount')

    result = await db.Transaction.create()
    ret = transaction_schema.dump(result)
    return json(ret)


async def get_transaction_by_id(request, id):
    result = await db.Transaction.get_by_id(id)
    ret = transaction_schema.dump(result)
    return json(ret)


async def get_all_transactions(request):
    result = await db.Transaction.get_all()
    ret = transaction_schema.dump(result)
    return json(ret)
