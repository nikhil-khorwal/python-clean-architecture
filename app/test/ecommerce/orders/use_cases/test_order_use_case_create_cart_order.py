import copy
from unittest import TestCase

from flask import current_app
from app.core.error.response import ResponseTypes

from app.ecommerce.order.requests.order_request import validate_order_create_data
from app.ecommerce.order.use_cases.create_cart_order_use_case import create_cart_order_use_case
from app.test.ecommerce.utils.sample_data.order_data import (
    order_request
)
from app.test.ecommerce.utils.sample_data.method import (
    create_address,
    create_admin_user,
    create_cart,
    create_category,
    create_product,
)

class TestOrderUseCaseCreateCartOrder(TestCase):
    def setUp(self):
        self.payload = order_request
        self.user = create_admin_user()
        self.address = create_address(self.user["email"])
        self.category = create_category()
        self.product = create_product(self.category["id"])
        self.cart = create_cart(self.product["id"],self.user["email"])
        

    def test_create_cart_order_with_invalid_data(self):
        with current_app.test_request_context("/?user_email={}".format(self.user["email"])):
            data = copy.deepcopy(self.payload)
            data.update({"address_id":"sds"})
            req = validate_order_create_data(data)
            res = create_cart_order_use_case(req)
            self.assertEqual(res.type, ResponseTypes.BADREQUEST_ERROR)

    def test_create_cart_order_with_valid_data(self):
        with current_app.test_request_context("/?user_email={}".format(self.user["email"])):
            data = copy.deepcopy(self.payload)
            data.update({"address_id":self.address["id"]})
            req = validate_order_create_data(data)
            res = create_cart_order_use_case(req)
            self.assertEqual(res.type, ResponseTypes.SUCCESS)
        