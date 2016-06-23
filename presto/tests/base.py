from flask_testing import TestCase, LiveServerTestCase
from presto import app, models
from presto.database import db_session, Base
from presto.admin.views import admin
from sqlalchemy import create_engine
from selenium import webdriver
from selenium.webdriver.chrome import service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import Select


class BaseTestCase(TestCase):

    def create_app(self):
        app.config.from_object('presto.settings.TestConfig')
        self.test_engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        return app

    def setUp(self):
        db_session.remove()
        db_session.configure(bind=self.test_engine)
        Base.metadata.create_all(self.test_engine)

        role1 = models.Role('admin')
        role2 = models.Role('client')

        db_session.add(role1)
        db_session.add(role2)
        db_session.commit()

        user = models.User('danzaw', 'danzaw@mail.pl',
                           "it's a secret", role_id=role1.id)
        user2 = models.User('himon', 'himon@mail.pl',
                            "it's a secret", role_id=role2.id)

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

    def tearDown(self):
        db_session.remove()
        Base.metadata.drop_all(self.test_engine)


class LiveServerBaseTestCase(LiveServerTestCase, BaseTestCase):

    def create_app(self):
        app.config.from_object('presto.settings.TestConfig')
        self.live_server_url = 'http://localhost:' + \
            str(app.config['LIVESERVER_PORT'])
        self.test_engine = create_engine(
            app.config['SQLALCHEMY_DATABASE_URI2'])
        db_session.remove()
        db_session.configure(bind=self.test_engine)

        return app

    def setUp(self):
        capabilities = DesiredCapabilities.CHROME
        command_executor = 'http://127.0.0.1:9515'
        self.browser = webdriver.Remote(command_executor, capabilities)
        # self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

        self.addCleanup(db_session.remove)
        self.addCleanup(Base.metadata.reflect, self.test_engine)
        self.addCleanup(Base.metadata.drop_all, self.test_engine)
        self.addCleanup(self.browser.quit)

        super().setUp()

    def tearDown(self):
        db_session.remove()
        Base.metadata.reflect(self.test_engine)
        Base.metadata.drop_all(self.test_engine)

        self.browser.quit()
