import copy
from unittest import TestCase

from app.ecommerce.order.requests.order_request import validate_order_create_data
from app.test.ecommerce.utils.sample_data.order_data import (
    order_request
)


class TestOrderRequest(TestCase):
    def setUp(self):
        self.payload = order_request

    def test_validate_order_request_with_invalid_data(self):
        data = copy.deepcopy(self.payload)
        data.update({"address_id":"sddsd"})
        req = validate_order_create_data(data)
        self.assertTrue(req.has_errors())
        self.assertFalse(req)

    def test_validate_order_request_with_valid_data(self):
        data = copy.deepcopy(self.payload)
        data.update({"address_id":34})
        req = validate_order_create_data(data)
        self.assertTrue(req)
        