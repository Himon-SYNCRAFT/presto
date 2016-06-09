from flask.ext.testing import TestCase
from presto import app, models
from presto.database import db_session, Base
from sqlalchemy import create_engine


class BaseTestCase(TestCase):

    def create_app(self):
        app.config.from_object('presto.settings.TestConfig')
        return app

    def setUp(self):

        self.test_engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

        db_session.configure(bind=self.test_engine)
        Base.metadata.create_all(self.test_engine)

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

        auction_type1 = models.AuctionType('sklepowa')
        auction_type2 = models.AuctionType('zwykła')

        db_session.add(auction_type1)
        db_session.add(auction_type2)

        db_session.commit()

    def tearDown(self):
        db_session.remove()
        Base.metadata.drop_all(self.test_engine)
