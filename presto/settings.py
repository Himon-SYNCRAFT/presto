# default config
class BaseConfig:
    DEBUG = False
    # shortened for readability
    SECRET_KEY = '$2a$12$9I0GUWWW8BqiQzJHwOB5Te3gtqzTiPT8uqqi5M9HNsITLSmPAx59K'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Awarene$4@localhost/presto'


class TestConfig(BaseConfig):
    DEBUG = False # Switch to False because if true flask_testing LiveServerTestCase run twice for whatever reason...
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    LIVESERVER_PORT = 8943
    SERVER_NAME  = 'localhost:' + str(LIVESERVER_PORT)


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False
