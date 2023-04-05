import copy
from unittest import TestCase
import pytest
from app.ecommerce.product.requests.product_request import validate_product_data
from app.test.ecommerce.utils.sample_data.product_data import product_request
from app.ecommerce.product.repository.product_repository import ProductRepository



class TestProductRequest(TestCase):
    def setUp(self):
        self.payload = product_request
        self.repo = ProductRepository()

    def test_validate_product_request_with_empty_field(self):
        data = copy.deepcopy(self.payload)
        data.update({"title": ""})
        req = validate_product_data(data)
        self.assertTrue(req.has_errors())

    def test_validate_product_request_with_invalid_id(self):
        req = validate_product_data(self.payload, "As")
        self.assertTrue(req.has_errors())
