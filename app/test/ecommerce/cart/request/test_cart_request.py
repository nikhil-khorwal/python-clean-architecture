import copy
from unittest import TestCase

from flask import current_app
from app.core.error.response import ResponseTypes
from app.ecommerce.cart.requests.cart_create_request_check import validate_cart_create_data, validate_cart_update_data
from app.ecommerce.cart.use_cases.add_product_to_cart_use_case import add_product_to_cart_use_case
from app.ecommerce.cart.use_cases.update_quantity_of_cart_use_case import update_quantity_of_cart_use_case

from app.test.ecommerce.utils.sample_data.method import (
    create_address,
    create_admin_user,
    create_cart,
    create_category,
    create_product,
)
from app.test.ecommerce.utils.sample_data.cart_data import (
    cart_request
)


class TestCartRequest(TestCase):
    def setUp(self):
        self.payload = cart_request

    def test_validate_cart_request_with_invalid_data(self):
        data = copy.deepcopy(self.payload)
        data.update({"product_id":"sddsd"})
        req = validate_cart_create_data(data)
        self.assertTrue(req.has_errors())
        self.assertFalse(req)

    def test_validate_cart_request_with_valid_data(self):
        data = copy.deepcopy(self.payload)
        data.update({"product_id":34})
        req = validate_cart_create_data(data)
        self.assertTrue(req)
        
    def test_validate_cart_update_request_with_invalid_data(self):
        data = copy.deepcopy(self.payload)
        cart_item_id = "df"
        data.update({"quantity":3})
        req = validate_cart_update_data(data,cart_item_id)
        self.assertTrue(req.has_errors())
        self.assertFalse(req)

    def test_validate_cart_update_request_with_valid_data(self):
        data = copy.deepcopy(self.payload)
        cart_item_id = 12
        data.update({"quantity":3})
        req = validate_cart_update_data(data,cart_item_id)
        self.assertTrue(req)
        