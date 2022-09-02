import requests
import random
import time


def create_dummy_uers():
    url = 'http://127.0.0.1:8000/api/users'
    for i in range(5):
        start = time.time()
        i += 1
        username = f'testuser{i}'
        password = f'testpass{i}'
        response = requests.post(url=url, json={'username': username, 'password': password})
        print(response.status_code, time.time() -start)

def create_dummy_bills():
    url = 'http://127.0.0.1:8000/api/bills'
    for i in range(3):
        start = time.time()
        user_id = 1
        response = requests.post(url=url, json={'user_id': user_id})
        print(response.status_code, time.time() - start)

def create_dummy_transactions():
    url = 'http://127.0.0.1:8000/api/transactions'
    for i in range(3):
        i += 1
        start = time.time()
        response = requests.post(url=url, json={"transfered": int(f'{i}00'), "bill_id": 1})
        print(response.status_code, time.time() - start)


def create_dummy_products():
    url = 'http://127.0.0.1:8000/api/products'
    for i in range(5):
        i += 1
        start = time.time()
        response = requests.post(url=url, json={"description": f'product descriprion {i}', "name": f'product{i}', 'price': float(f"{i}00.99")})
        print(response.status_code, time.time() - start)

if __name__ == '__main__':
    create_dummy_uers()
    # create_dummy_bills()
    # create_dummy_transactions()
    create_dummy_products()
