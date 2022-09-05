import aiohttp
from Crypto.Hash import SHA
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


async def paymen_webhook(user_id, bill_id, transaction_id, amount):
    private_key = 'private_key'
    signature = SHA.new(f'{private_key}:{transaction_id}:{bill_id}:{amount}'.encode()).hexdigest()
    body = {'signature': signature,
                    'user_id': user_id,
                    'bill_id': bill_id,
                    'amount': amount,
                }
    async with aiohttp.ClientSession() as session:
        await session.post('http://127.0.0.1:5000/payment/webhook', json=body)
    

async def add_funds(request):
    user_id = request.json.get('user_id', None)
    bill_id = request.json.get('bill_id', None)
    amount = request.json.get('amount', None)

    if not bill_id:
        raise BadRequest('Pls provice bill_id')
    if not user_id:
        raise BadRequest('Pls provice user_id')
    if not amount:
        raise BadRequest('Pls provice amount')

    bill: db.Bill = await db.Bill.get_bill_by_id(bill_id)
    bill = bill_schema.dump(bill)
    if not bill:
        print('creating new bill')
        bill = await db.Bill.create(user_id=user_id)
        bill = bill_schema.dump(bill)

    balance = bill['balance'] + amount
    await db.Bill.update(bill_id, balance=balance)
    result = await db.Transaction.create(transfered=amount, bill_id=bill_id)
    transaction_id = result['id']
    await paymen_webhook(user_id=user_id, bill_id=bill_id, transaction_id=transaction_id, amount=amount)
    return json({'success': True, 'message': f'Transfered: {amount}'})
