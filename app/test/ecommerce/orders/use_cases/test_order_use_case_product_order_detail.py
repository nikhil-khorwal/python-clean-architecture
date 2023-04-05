from unittest import TestCase

from flask import current_app
from app.core.error.response import ResponseTypes
from app.core.methods.core_method import validate_params_id
from app.ecommerce.order.use_cases.product_order_detail_use_case import product_order_detail_use_case

from app.test.ecommerce.utils.sample_data.method import (
    create_address,
    create_admin_user,
    create_cart,
    create_order,
    create_category,
    create_product,
)
from app.test.ecommerce.utils.sample_data.order_data import (
    order_request
)


class TestOrderUseCaseProductOrderDetail(TestCase):
    def setUp(self):
        self.payload = order_request
        self.user = create_admin_user()
        self.category = create_category()
        self.product = create_product(self.category["id"])

    def test_get_product_order_detail_with_invalid_request(self):
        with current_app.test_request_context("/?user_email={}".format(self.user["email"])):
            req = validate_params_id("sdsd")
            res = product_order_detail_use_case(req)
            self.assertEqual(res.type, ResponseTypes.BADREQUEST_ERROR)

    def test_get_product_order_detail_with_valid_request(self):
        with current_app.test_request_context("/?user_email={}".format(self.user["email"])):
            req = validate_params_id(self.product["id"])
            res = product_order_detail_use_case(req)
            self.assertEqual(res.type, ResponseTypes.SUCCESS)
