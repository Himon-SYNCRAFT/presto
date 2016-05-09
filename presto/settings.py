# default config
class BaseConfig:
    DEBUG = False
    # shortened for readability
    SECRET_KEY = '$2a$12$9I0GUWWW8BqiQzJHwOB5Te3gtqzTiPT8uqqi5M9HNsITLSmPAx59K'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Awarene$4@localhost/presto'


class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False
