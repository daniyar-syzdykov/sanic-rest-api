import json
import random
from routes import *
from sanic import Sanic, response
from routes import api
from sanic_jwt import Initialize
from database.utils import async_db_session as session
from views import store_token, get_refresh_token, authenticate, retrieve_user
from string import ascii_lowercase, digits
import database as db
from database.schemas import *


# @pytest.fixture
def init_app():
    sanic_app = Sanic('testing')
    sanic_app.blueprint(api)
    Initialize(sanic_app,
               authenticate=authenticate,
               refresh_token_enabled=True,
               store_refresh_token=store_token,
               retrieve_refresh_token=get_refresh_token,
               retrieve_user=retrieve_user
               )

    @sanic_app.before_server_start
    async def connect(app):
        await session.init()
        await session.create_all()

    return sanic_app


sanic_app = init_app()


def random_user_credantials() -> tuple[str, str]:
    username = ''
    password = ''
    n = random.randrange(1, 15)
    for i in range(n):
        username += random.choice(ascii_lowercase + digits)
        password += random.choice(ascii_lowercase + digits)
    return (username, password)
