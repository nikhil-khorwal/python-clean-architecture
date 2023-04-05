from asyncio import CancelledError
from email.policy import default
import enum
from flask import current_app
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column,
    Enum,
    ForeignKey,
    Integer,
    String,
    column,
    create_engine,
    Boolean,
    null,
    Float,
)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.inspection import inspect
import os
from sqlalchemy.orm import relationship
from datetime import datetime
from app.ecommerce.product.domain.product_domain import ProductDomain

Base = declarative_base()


class OrderEnum(enum.Enum):
    CANCELLED = "cancelled"
    SUCCESS = "success"
    PENDING = "pending"


class PostgresConfiguration:
    db = dict()

    def __init__(self):
        self.__dict__ = self.db
        connection_string = "postgresql+psycopg2://{}:{}@{}:{}".format(
            current_app.config["POSTGRES_USER"],
            current_app.config["POSTGRES_PASSWORD"],
            current_app.config["POSTGRES_HOSTNAME"],
            current_app.config["POSTGRES_PORT"],
        )

        engine = create_engine(connection_string)
        metadata = Base.metadata.create_all(engine)
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()

    def __str__(self):
        return self.session

    @staticmethod
    def get_session():
        if len(PostgresConfiguration.db) == 0:
            PostgresConfiguration()
        return PostgresConfiguration.db["session"]


class UserTable(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    phone = Column(String(15))
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(150))

    is_admin = Column(Boolean, default=False)
    is_delete = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    created_at = Column(String(100), default=datetime.now())
    updated_at = Column(String(100), default=datetime.now())
    carts = relationship("CartTable", backref="users")
    orders = relationship("OrderTable", backref="users")
    addresses = relationship("AddressTable", backref="users")


class AddressTable(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True, autoincrement=True)
    house_no = Column(String(100))
    street = Column(String(250))
    landmark = Column(String(200))
    pincode = Column(Integer)
    city = Column(String(100))
    state = Column(String(100))
    user_id = Column(
        Integer, ForeignKey(UserTable.id, ondelete="CASCADE"), nullable=True)
    created_at = Column(String(100), default=datetime.now())
    updated_at = Column(String(100), default=datetime.now())
    is_delete = Column(Boolean, default=False)
    orders = relationship("OrderTable", backref="address")


class CategoryTable(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100))
    created_at = Column(String(100), default=datetime.now())
    updated_at = Column(String(100), default=datetime.now())
    is_delete = Column(Boolean, default=False)
    products = relationship("ProductTable", backref="categories")


class ProductTable(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100))
    desc = Column(String(250))
    price = Column(Integer)
    discount_percentage = Column(Float)
    gst_percentage = Column(Float)
    stock = Column(Integer)
    category_id = Column(Integer, ForeignKey(CategoryTable.id, ondelete="CASCADE"))
    carts = relationship("CartItemTable", backref="products")
    orders = relationship("OrderItemTable", backref="products")
    images = relationship("ImageTable", backref="products")
    created_at = Column(String(100), default=datetime.now())
    updated_at = Column(String(100), default=datetime.now())
    is_delete = Column(Boolean, default=False)


class CartTable(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(UserTable.id, ondelete="CASCADE"))
    cart_items = relationship("CartItemTable", backref="carts")
    created_at = Column(String(100), default=datetime.now())
    updated_at = Column(String(100), default=datetime.now())
    is_delete = Column(Boolean, default=False)


class CartItemTable(Base):
    __tablename__ = "cartItem"

    id = Column(Integer, primary_key=True, autoincrement=True)
    quantity = Column(Integer)
    cart_id = Column(Integer, ForeignKey(CartTable.id, ondelete="CASCADE"))
    product_id = Column(Integer, ForeignKey(ProductTable.id, ondelete="CASCADE"))
    created_at = Column(String(100), default=datetime.now())
    updated_at = Column(String(100), default=datetime.now())


class PaymentTable(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    price = Column(Float)
    discount_price = Column(Float)
    sub_total = Column(Float)
    gst_price = Column(Float)
    net_price = Column(Float)
    orders = relationship("OrderTable", backref="payments")
    is_delete = Column(Boolean, default=False)


class OrderTable(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(100))
    phone = Column(String(13))
    user_id = Column(Integer, ForeignKey(UserTable.id, ondelete="CASCADE"))
    address_id = Column(Integer, ForeignKey(AddressTable.id, ondelete="CASCADE"))
    created_at = Column(String(100), default=datetime.now())
    updated_at = Column(String(100), default=datetime.now())
    status = Column(Enum(OrderEnum))
    payment_id = Column(Integer, ForeignKey(PaymentTable.id, ondelete="CASCADE"))
    order_items = relationship("OrderItemTable", backref="orders")
    is_delete = Column(Boolean, default=False)


class OrderItemTable(Base):
    __tablename__ = "orderItem"

    id = Column(Integer, primary_key=True, autoincrement=True)
    quantity = Column(Integer)
    order_id = Column(Integer, ForeignKey(OrderTable.id, ondelete="CASCADE"))
    product_id = Column(Integer, ForeignKey(ProductTable.id, ondelete="CASCADE"))
    created_at = Column(String(100), default=datetime.now())
    updated_at = Column(String(100), default=datetime.now())
    is_delete = Column(Boolean, default=False)


class ImageTable(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, autoincrement=True)
    file_name = Column(String(150))
    file_path = Column(String(300))
    product_id = Column(Integer, ForeignKey(ProductTable.id, ondelete="CASCADE"))
    created_at = Column(String(100), default=datetime.now())
    updated_at = Column(String(100), default=datetime.now())
    is_delete = Column(Boolean, default=False)
