from datetime import datetime
from sanic_jwt import Initialize
from sanic import Sanic
from views import store_token, retrive_refresh_token, authenticate, retrieve_user, generate_refresh_token, CustomResponses
from database.utils import async_db_session as session
from routes import api

app = Sanic('test_app')
app.blueprint(api)

Initialize(app,
        authenticate=authenticate,
        refresh_token_enabled=True,
        store_refresh_token=store_token,
        retrieve_refresh_token=retrive_refresh_token,
        retrieve_user=retrieve_user,
        responses_class=CustomResponses,
        generate_refresh_token=generate_refresh_token
    )


@app.after_server_start
async def init(app):
    # valid = await app.ctx.auth.verify_token('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE2NjIyODM4NzZ9.vHxjbzR9N15ZTZyHFQhOw5WD8Yw-JySD2IIb9uXi5xs')
    # print(valid)
    # print(app.ctx.expiration_delta)
    await session.init()
    await session.create_all()

if __name__ == '__main__':
    # app.run(dev=True)
    app.run()
