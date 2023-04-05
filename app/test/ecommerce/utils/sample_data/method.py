import copy
import json
from flask import current_app
import pytest

from app.ecommerce.address.repository.address_repository import AddressRepository
from app.ecommerce.address.requests.address_request import validate_create_address_data
from app.ecommerce.cart.repository.cart_repository import CartRepository
from app.ecommerce.cart.serializers.cart_serializer import CartAdminSerializer, CartSerializer
from app.ecommerce.category.repository.category_repository import CategoryRepository
from app.ecommerce.order.repository.order_repository import OrderRepository
from app.ecommerce.order.serializers.order_serializer import OrderSerializer
from app.ecommerce.product.repository.product_repository import ProductRepository

from app.ecommerce.user.repository.user_repository import UserRepository
from app.test.ecommerce.utils.sample_data.email_generator import generate_random_emails
from app.test.ecommerce.utils.sample_data.user_data import test_user_request
from app.test.ecommerce.utils.sample_data.address_data import address_request
from app.test.ecommerce.utils.sample_data.product_data import product_request
from app.test.ecommerce.utils.sample_data.category_data import category_request
from app.test.ecommerce.utils.sample_data.cart_data import cart_request
from app.test.ecommerce.utils.sample_data.order_data import order_request

def create_user():
    user_repo = UserRepository()
    test_user_request["email"] = generate_random_emails()
    test_user_request["is_admin"] = False
    test_user = user_repo.user_sign_up(test_user_request)
    user= test_user.value["data"].to_dict()
    return user

def create_admin_user():
    user_repo = UserRepository()
    test_user_request["email"] = generate_random_emails()
    test_user_request["is_admin"] = True
    test_user = user_repo.user_sign_up(test_user_request)
    user= test_user.value["data"].to_dict()
    return user

def create_address(user_email):
    address_repo = AddressRepository()
    with current_app.test_request_context("/?user_email={}".format(user_email)):
        test_address = address_repo.create_address(address_request)
        address= test_address.value["data"].to_dict()
        return address

def create_product(category_id):
    product_repo = ProductRepository()
    data = copy.deepcopy(product_request)
    data["category_id"] = category_id
    test_product = product_repo.create_product(data)
    product= test_product.value["data"].to_dict()
    return product

def create_category():
    category_repo = CategoryRepository()
    test_category = category_repo.create_category(category_request)
    category= test_category.value["data"].to_dict()
    return category

def create_cart(product_id, user_email):
    with current_app.test_request_context("/?user_email={}".format(user_email)):
        cart_repo = CartRepository()
        data = copy.deepcopy(cart_request)
        data.update({"product_id":product_id})
        test_cart = cart_repo.add_product_to_cart(data)
        cart= cart_repo.get_user_cart()
        return json.loads(json.dumps(cart.value,cls=CartAdminSerializer))

def create_order(address_id, user_email):
    with current_app.test_request_context("/?user_email={}".format(user_email)):
        order_repo = OrderRepository()
        data = copy.deepcopy(order_request)
        data.update({"address_id":address_id})
        test_order = order_repo.create_cart_order(data)
        order = json.loads(json.dumps(test_order.value,cls=OrderSerializer))
        return order["data"]