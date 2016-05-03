from presto import bcrypt
from presto.database import Base
from sqlalchemy import Column, Integer, String, Binary, CHAR, ForeignKey, Float, \
    Boolean, Table, Numeric, Text, DateTime
from sqlalchemy.orm import relationship
from hashlib import sha256
from base64 import b64encode


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    login = Column(String(128), unique=True, nullable=False)
    mail = Column(String(256), unique=True, nullable=False)
    password_hash = Column(Binary(60), nullable=False)

    def __init__(self, login, mail, password):
        self.login = login
        self.mail = mail
        self.generate_password_hash(password)

    def generate_password_hash(self, password):
        self.password_hash = bcrypt.generate_password_hash(password)

    def check_password_hash(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)


class Account(Base):
    __tablename__ = 'account'

    id = Column(Integer, primary_key=True)
    name = Column(String(16), unique=True, nullable=False)
    mail = Column(String(256), unique=True, nullable=False)
    password_hash = Column(Binary(64), nullable=False)
    webapi_key = Column(String(32), nullable=False)

    def __init__(self, name, mail, password, webapi_key):
        self.name = name
        self.mail = mail
        self.webapi_key = webapi_key
        self._generate_password_hash(password)

    def _generate_password_hash(self, password):
        password = password.encode('utf-8')
        self.password_hash = b64encode(
            sha256(password).hexdigest().encode('utf-8'))


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(128), unique=True, nullable=False)

    parent_id = Column(Integer, ForeignKey('category.id'))

    children = relationship("Category")
    products = relationship('Product', back_populates='category')


class CategoryAttribute(Base):
    __tablename__ = 'category_attribute'

    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    name = Column(String(128), nullable=False)


class DeliveryTimeType(Base):
    __tablename__ = 'delivery_time_type'

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False, unique=True)


class CategoryAttributeValue(Base):
    __tablename__ = 'category_attribute_value'

    value = Column(String(128))

    product_id = Column(Integer, ForeignKey('product.id'),
                        nullable=False, primary_key=True)
    category_attribute_id = Column(Integer, ForeignKey(
        'category_attribute.id'), nullable=False, primary_key=True)


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    name = Column(String(128), unique=True, nullable=False)
    sku = Column(Integer, nullable=False, unique=True)
    short_description = Column(Text)

    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    delivery_time_type_id = Column(
        Integer, ForeignKey('delivery_time_type.id'))

    prices = relationship('ProductPrice')
    titles = relationship('ProductTitle')
    auctions = relationship('Auction')
    category = relationship('Category', back_populates='products')
    category_attributes_values = relationship('CategoryAttributeValue')
    delivery_time_type = relationship('DeliveryTimeType')
    shipping_values = relationship('ShippingValue')
    images = relationship('ProductImage')
    description = relationship('DescriptionBlock')


class ProductPrice(Base):
    __tablename__ = 'product_price'

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=True)
    value = Column(Numeric(12, 2), nullable=False)
    is_default = Column(Boolean, nullable=False, default=False)

    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)


class ShippingType(Base):
    __tablename__ = 'shipping_type'

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False, unique=True)
    is_boolean = Column(Boolean, nullable=False, default=False) # odbiory osobiste itp jako checkboxy


class ShippingValue(Base):
    __tablename__ = 'shipping_value'

    first_item = Column(Numeric(12, 2), nullable=False, default=-1.00)
    next_item = Column(Numeric(12, 2), nullable=False, default=-1.00)
    quantity = Column(Numeric(12, 2), nullable=False, default=-1)

    product_id = Column(Integer, ForeignKey('product.id'),
                        nullable=False, primary_key=True)
    shipping_type_id = Column(Integer, ForeignKey(
        'shipping_type.id'), nullable=False, primary_key=True)

    product = relationship('Product')


class ProductTitle(Base):
    __tablename__ = 'product_title'

    id = Column(Integer, primary_key=True)

    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)


class Auction(Base):
    __tablename__ = 'auction'

    id = Column(Integer, primary_key=True)
    alternative_title = Column(String(128))
    alternative_mini_img_url = Column(String(128))
    prolong = Column(Boolean, nullable=False, default=True)
    featured = Column(Boolean, nullable=False, default=False)
    auction_number = Column(Integer, nullable=True, default=None)
    date = Column(DateTime, nullable=False)

    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    location_id = Column(Integer, ForeignKey('location.id'), nullable=False)
    auction_type_id = Column(Integer, ForeignKey(
        'auction_type.id'), nullable=False)
    duration_type_id = Column(Integer, ForeignKey(
        'auction_duration.id'), nullable=False)
    account_id = Column(Integer, ForeignKey('account.id'), nullable=False)

    location = relationship('Location')
    auction_type = relationship('AuctionType')
    account = relationship('Account')


class Location(Base):
    __tablename__ = 'location'

    id = Column(Integer, primary_key=True)
    name = Column(String(128), unique=True, nullable=False)


class AuctionType(Base):
    __tablename__ = 'auction_type'

    id = Column(Integer, primary_key=True)
    name = Column(String(128))


class AuctionDuration(Base):
    __tablename__ = 'auction_duration'

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)


class ProductImage(Base):
    __tablename__ = 'product_image'

    id = Column(Integer, primary_key=True)
    url = Column(String(1024))
    is_thumbnail = Column(Boolean, nullable=False, default=False)

    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)


class DescriptionBlockType(Base):
    __tablename__ = 'description_block_type'

    id = Column(Integer, primary_key=True)
    definition = Column(Text)
    css_class = Column(String(32))


class DescriptionBlock(Base):
    __tablename__ = 'description_block'

    id = Column(Integer, primary_key=True)
    header_1 = Column(String(128))
    header_2 = Column(String(128))
    img_1 = Column(String(128))
    img_2 = Column(String(128))
    text_1 = Column(Text)
    text_2 = Column(Text)
    sort = Column(Integer, nullable=False, default=0)
    is_short_description = Column(Boolean, nullable=False, default=False)
    css_class = Column(String(32))

    description_block_type_id = Column(Integer, ForeignKey(
        'description_block_type.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
