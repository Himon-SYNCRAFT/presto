from presto import app
from presto.allegro_client.client import AllegroClient


@app.route('/')
def index():
    webapi_key = app.config['WEBAPI_KEY']
    login = app.config['LOGIN']
    password = app.config['PASSWORD']

    client = AllegroClient()

    return client.login(webapi_key, login, password), 200
