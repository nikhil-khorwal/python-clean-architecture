from unittest import TestCase

from flask import current_app
from app.core.error.response import ResponseTypes
from app.ecommerce.order.use_cases.cart_order_detail_use_case import cart_order_detail_use_case

from app.test.ecommerce.utils.sample_data.method import (
    create_admin_user
)


class TestOrderUseCaseCancleOrder(TestCase):
    def setUp(self):
        self.user = create_admin_user()
    
    def test_get_cart_order_detail(self):
        with current_app.test_request_context("/?user_email={}".format(self.user["email"])):
            res = cart_order_detail_use_case()
            self.assertEqual(res.type, ResponseTypes.SUCCESS)
