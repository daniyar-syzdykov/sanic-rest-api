from sanic_jwt import Initialize
from sanic import Sanic
from views import store_token, get_token, authenticate, retrieve_user
from database.utils import async_db_session as session
from routes import api

app = Sanic('test_app')
app.blueprint(api)

Initialize(app,
        authenticate=authenticate,
        refresh_token_enabled=True,
        store_refresh_token=store_token,
        retrieve_refresh_token=get_token,
        retrieve_user=retrieve_user
    )


@app.after_server_start
async def init(app):
    await session.init()
    await session.create_all()

if __name__ == '__main__':
    app.run(dev=True)
