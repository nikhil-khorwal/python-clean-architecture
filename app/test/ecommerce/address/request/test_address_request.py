import copy
from unittest import TestCase
import pytest
from app.ecommerce.address.requests.address_request import validate_address_data, validate_create_address_data
from app.test.ecommerce.utils.sample_data.address_data import address_request




class TestaddressRequest(TestCase):
    def setUp(self):
        self.payload = address_request

    def test_validate_address_request_with_empty_field(self):
        data = copy.deepcopy(self.payload)
        data.update({"pincode": ""})
        req = validate_create_address_data(data=data)
        self.assertTrue(req.has_errors())
    
    def test_validate_address_request_with_reuired_field(self):
        data = copy.deepcopy(self.payload)
        data.pop("pincode")
        req = validate_create_address_data(data=data)
        self.assertTrue(req.has_errors())

    def test_validate_address_request_with_invalid_id(self):
        req = validate_address_data(data=self.payload, id="As")
        self.assertTrue(req.has_errors())
