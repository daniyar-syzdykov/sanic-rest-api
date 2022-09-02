from sanic import Blueprint
from views import *


api = Blueprint('api', url_prefix='/api')


# User routes
api.add_route(get_all_users, '/users', methods=('GET', ))
api.add_route(create_user, '/users', methods=('POST', ))
api.add_route(get_user_by_id, '/users/<user_id:int>', methods=('GET', ))
api.add_route(activate_user, '/users/activate/<uuid:slug>', methods=('PATCH', ))
api.add_route(delete_user, '/users/delete/<id:int>', methods=('DELETE', ))


# Bill routes
api.add_route(get_all_bills, '/bills', methods=('GET', ))
api.add_route(create_bill, '/bills', methods=('POST', ))
api.add_route(add_funds, '/bills/add/', methods=('POST', ))
api.add_route(get_bill_by_id, '/bills/<id:int>', methods=('GET', ))
# api.add_route(update_bill_balance, '/bills/<id:int>', methods=('PATCH', ))
# api.add_route(delete_bill, '/bills/<id:int>', methods=('DELETE', ))


# Trancation routes
api.add_route(get_all_transactions, '/transactions', methods=('GET', ))
api.add_route(create_transaction, '/transactions', methods=('POST', ))
api.add_route(get_transaction_by_id, '/transactions/<id:int>', methods=('GET', ))
# api.add_route(delete_transaction, '/transactions/<id:int>', methods=('DELETE', ))

# Product routes
api.add_route(get_all_products, '/products', methods=('GET', ))
api.add_route(create_product, '/products', methods=('POST', ))
api.add_route(get_product_by_id, '/products/<id:int>', methods=('GET', ))
api.add_route(delete_product, '/products/<id:int>', methods=('DELETE', ))
api.add_route(buy_product, '/products/<product_id:int>/buy', methods=('POST', ))
