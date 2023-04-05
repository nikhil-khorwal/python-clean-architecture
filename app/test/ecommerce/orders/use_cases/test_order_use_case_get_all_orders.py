from unittest import TestCase

from flask import current_app
from app.core.error.response import ResponseTypes
from app.core.methods.core_method import validate_params_id
from app.ecommerce.order.use_cases.get_all_orders_use_case import get_all_orders_use_case

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


class TestOrderUseCaseGetAllOrders(TestCase):
    def setUp(self):
        self.payload = order_request
        self.user = create_admin_user()
      
    def test_get_all_order_with_invalid_request(self):
        with current_app.test_request_context("/?user_email={}".format(self.user["email"])):
            res = get_all_orders_use_case()
            self.assertEqual(res.type, ResponseTypes.SUCCESS)
