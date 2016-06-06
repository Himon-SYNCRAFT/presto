import unittest

from flask.ext.script import Manager
from presto import app, models
from presto.database import Base, db_session
from presto.tests import functional_tests

manager = Manager(app)


@manager.command
def test(case_name=None):
    """Runs the unit tests."""
    if case_name is not None:
        tests = unittest.TestLoader().discover(
            'presto/tests', pattern='test*' + case_name + '.py')
    else:
        tests = unittest.TestLoader().discover('presto/tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def func_tests(case_name=None):
    """Runs the functional tests with Selenium"""
    if case_name is None:
        tests = unittest.TestLoader().loadTestsFromModule(functional_tests)
    else:
        tests = unittest.TestLoader().loadTestsFromName('presto.tests.functional_tests.' + case_name)
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

    account = models.Account('danzaw', 'danzaw@gmail.com',
                             "it's a secret", 'webapi_key')

    db_session.add(account)
    db_session.commit()

    shipping_type1 = models.ShippingType('Kurier', False)
    shipping_type2 = models.ShippingType('Odbiór osobisty', True)

    db_session.add(shipping_type1)
    db_session.add(shipping_type2)

    db_session.commit()


if __name__ == '__main__':
    manager.run()
