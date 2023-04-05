import pytest
from app.core.methods.core_method import validate_params_id
from app.ecommerce.category.repository.category_repository import (
    CategoryRepository
)
from app.ecommerce.category.use_cases.category_delete_use_case import (
    category_delete_use_case
)
from app.test.ecommerce.utils.sample_data.category_data import (
    category_request
)
from app.core.error.response import ResponseTypes
from unittest import TestCase




class TestCategoryDeleteUseCase(TestCase):
    def setUp(self):
        self.payload = category_request
        self.cat_repo = CategoryRepository()
        self.test_category = self.cat_repo.create_category(category_request)

    def test_delete_category_by_invalid_id(self):
        req_id = validate_params_id("sad")
        res = category_delete_use_case(req_id)
        assert res.type == ResponseTypes.BADREQUEST_ERROR

    def test_delete_category_by_id(self):
        req_id = validate_params_id(self.test_category.value["data"].id)
        res = category_delete_use_case(req_id)
        assert res.value["message"] == "delete category successfully"
