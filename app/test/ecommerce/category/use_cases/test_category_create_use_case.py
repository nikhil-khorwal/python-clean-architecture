import pytest
from app.ecommerce.category.repository.category_repository import (
    CategoryRepository
)
from app.ecommerce.category.use_cases.category_create_use_case import (
    category_create_use_case
)
from app.test.ecommerce.utils.sample_data.category_data import (
    category_request
)
from app.core.error.response import ResponseTypes
from app.ecommerce.category.requests.category_request import (
    validate_category_data
)


import copy
from unittest import TestCase




class TestCategoryCreateUseCase(TestCase):
    def setUp(self):
        self.payload = category_request
        self.cat_repo = CategoryRepository()
        self.test_category = self.cat_repo.create_category(category_request)

    def test_category_create_with_invalid_title(self):
        data = copy.deepcopy(self.payload)
        data["title"] = ""
        req = validate_category_data(data)
        res = category_create_use_case(req)
        assert res.type == ResponseTypes.BADREQUEST_ERROR

    def test_category_create_with_get_exception(self):
        data = copy.deepcopy(self.payload)
        data.pop('title')
        req = validate_category_data(data)
        res = category_create_use_case(req)
        assert res.type == ResponseTypes.SYSTEM_ERROR

    def test_category_create_with_valid_data(self):
        data = copy.deepcopy(self.payload)
        req = validate_category_data(data)
        res = category_create_use_case(req)

        assert res.type == ResponseTypes.SUCCESS
