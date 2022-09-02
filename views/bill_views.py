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


async def add_funds(request):
    user_id = request.json.get('user_id', None)
    bill_id = request.json.get('bill_id', None)
    amount = request.json.get('amount', None)

    if not bill_id: raise BadRequest('Pls provice bill_id')
    if not user_id: raise BadRequest('Pls provice user_id')
    if not amount: raise BadRequest('Pls provice amount')

    bill: db.Bill = await db.Bill.get_by_id(bill_id)
    if not bill:
        bill = await db.Bill.create(user_id=user_id)
    
    balance = bill.balance + amount
    await db.Bill.update(bill_id, balance=balance)
    await db.Transaction.create(transfered=amount, bill_id=bill_id)
    return json({'success': True, 'message': f'Transfered: {amount}'})
