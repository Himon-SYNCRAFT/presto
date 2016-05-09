from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config.from_object('presto.settings.DevelopmentConfig')
print(app.config['SQLALCHEMY_DATABASE_URI'])
bcrypt = Bcrypt(app)

from presto import views
