from unittest import TestCase

from flask import current_app
from app.core.error.response import ResponseTypes
from app.core.methods.core_method import validate_params_id
from app.ecommerce.cart.requests.cart_create_request_check import validate_cart_update_data
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


class TestCartUseCaseRemoveProductFromCart(TestCase):
    def setUp(self):
        self.payload = cart_request
        self.user = create_admin_user()
        self.address = create_address(self.user["email"])
        self.category = create_category()
        self.product = create_product(self.category["id"])
        self.cart = create_cart(self.product["id"],self.user["email"])
    
    def test_update_product_from_cart_with_invalid_request(self):
        with current_app.test_request_context("/?user_email={}".format(self.user["email"])):
            updated_data = {
                "quantity":1
            }
            req = validate_cart_update_data(updated_data, "sdsd")
            res = update_quantity_of_cart_use_case(req)
            self.assertEqual(res.type, ResponseTypes.BADREQUEST_ERROR)

    def test_update_product_from_cart_with_valid_request(self):
        with current_app.test_request_context("/?user_email={}".format(self.user["email"])):
            updated_data = {
                "quantity":1
            }
            req = validate_cart_update_data(updated_data,self.cart["cart_items"][0]["id"])
            res = update_quantity_of_cart_use_case(req)
            self.assertEqual(res.type, ResponseTypes.SUCCESS)
