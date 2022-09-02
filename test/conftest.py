import pytest
from routes import *
from sanic import Sanic, response
from routes import api
from sanic_testing import TestManager
from sanic_jwt import Initialize
from database.utils import async_db_session as session
from views import store_token, get_token, authenticate, retrieve_user
# from server import app as sanic_app, session


# @pytest.fixture
def app():
    print('initialaizing pytest fixture')
    sanic_app = Sanic('testing')
    sanic_app.blueprint(api)
    Initialize(sanic_app,
            authenticate=authenticate,
            refresh_token_enabled=True,
            store_refresh_token=store_token,
            retrieve_refresh_token=get_token,
            retrieve_user=retrieve_user
        )

    @sanic_app.before_server_start
    async def connect(app):
        await session.init()
        await session.create_all()

    return sanic_app

sanic_app = app()
