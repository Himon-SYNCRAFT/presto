from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = '$2a$12$9I0GUWWW8BqiQzJHwOB5Te3gtqzTiPT8uqqi5M9HNsITLSmPAx59K'
bcrypt = Bcrypt(app)

from presto import views
