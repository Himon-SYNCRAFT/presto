import unittest
import os
import signal
import subprocess
from flask.ext.script import Manager, Command, Option
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
    pro = subprocess.Popen('chromedriver --port=9515', stdout=subprocess.PIPE,
                           shell=True, preexec_fn=os.setsid)

    if case_name is None:
        tests = unittest.TestLoader().loadTestsFromModule(functional_tests)
    else:
        tests = unittest.TestLoader().loadTestsFromName(
            'presto.tests.functional_tests.' + case_name)
    unittest.TextTestRunner(verbosity=2).run(tests)

    os.killpg(os.getpgid(pro.pid), signal.SIGTERM)


@manager.add_command
class CommandWithCatchAll(Command):
    """Runs the tests

    Examples:
    python manage.py tests test_pyfile
    python manage.py tests test_pyfile TestCaseName
    python manage.py tests test_pyfile TestCaseName test_method"""

    capture_all_args = True
    name = 'tests'

    def run(self, remaining_args):
        tests_path = '.'.join(remaining_args)
        tests = unittest.TestLoader().loadTestsFromName('presto.tests.' + tests_path)
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

    role1 = models.Role('admin')
    role2 = models.Role('client')

    db_session.add(role1)
    db_session.add(role2)
    db_session.commit()


    user = models.User('danzaw', 'danzaw@mail.pl', "it's a secret", 1)
    user2 = models.User('himon', 'himon@mail.pl', "it's a secret", 2)

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

    auction_type1 = models.AuctionType('sklepowa')
    auction_type2 = models.AuctionType('zwykła')

    db_session.add(auction_type1)
    db_session.add(auction_type2)

    db_session.commit()


if __name__ == '__main__':
    manager.run()
