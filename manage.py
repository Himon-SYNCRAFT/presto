from presto import app, models
from presto.database import Base, db_session
from flask.ext.script import Manager
import unittest

manager = Manager(app)


@manager.command
def test():
    """Runs the unit tests without coverage."""
    tests = unittest.TestLoader().discover('presto/tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@manager.command
def run():
    """Starts server."""
    app.run(debug=True)

@manager.command
def create_db():
    Base.metadata.reflect()
    Base.metadata.drop_all()
    Base.metadata.create_all()

    user = models.User('danzaw', 'danzaw@mail.pl', "it's a secret")
    user2 = models.User('himon', 'himon@mail.pl', "it's a secret")

    db_session.add(user)
    db_session.add(user2)
    db_session.commit()

    account = models.Account('danzaw', 'danzaw@gmail.com', "it's a secret", 'webapi_key')

    db_session.add(account)
    db_session.commit()


if __name__ == '__main__':
    manager.run()
