import copy
from unittest import TestCase
import pytest
from app.ecommerce.category.requests.category_request import validate_category_data
from app.test.ecommerce.utils.sample_data.category_data import category_request
from app.ecommerce.category.repository.category_repository import (
    CategoryRepository
)



class TestcategoryRequest(TestCase):
    def setUp(self):
        self.payload = category_request
        self.repo = CategoryRepository()

    def test_validate_category_request_with_empty_field(self):
        data = copy.deepcopy(self.payload)
        data.update({"title": ""})
        req = validate_category_data(data=data, id="1")
        self.assertTrue(req.has_errors())

    def test_validate_category_request_with_invalid_id(self):
        req = validate_category_data(data=self.payload, id="As")
        self.assertTrue(req.has_errors())
