import copy
from unittest import TestCase

from flask import current_app
from flask import request
from app.core.error.response import ResponseTypes
from app.core.methods.core_method import validate_params_id
from app.ecommerce.cart.repository.cart_repository import CartRepository
from app.ecommerce.cart.requests.cart_create_request_check import validate_cart_create_data, validate_cart_update_data
from app.ecommerce.cart.use_cases.get_user_cart_use_case import get_user_cart_use_case
from app.ecommerce.cart.use_cases.update_quantity_of_cart_use_case import update_quantity_of_cart_use_case

from app.test.ecommerce.utils.sample_data.method import (
    create_address,
    create_admin_user,
    create_cart,
    create_category,
    create_product,
    create_user,
)
from app.test.ecommerce.utils.sample_data.cart_data import (
    cart_request
)


class TestCartUseCaseGetUserCart(TestCase):
    def setUp(self):
        self.payload = cart_request
        self.user = create_admin_user()
        self.user2 = create_user()
        self.address = create_address(self.user["email"])
        self.category = create_category()
        self.product = create_product(self.category["id"])
        self.cart = create_cart(self.product["id"],self.user["email"])
    
    def test_get_user_cart_with_empty_cart(self):
        with current_app.test_request_context("/?user_email={}".format(self.user2["email"])):
            res = get_user_cart_use_case() 
            self.assertEqual(res.type, ResponseTypes.SUCCESS)

    def test_get_user_cart_with_valid_email(self):
        with current_app.test_request_context("/?user_email={}".format(self.user["email"])):
            res = get_user_cart_use_case()
            self.assertEqual(res.type, ResponseTypes.SUCCESS)
