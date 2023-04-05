import pytest
from app.ecommerce.category.repository.category_repository import (
    CategoryRepository
)
from app.ecommerce.category.use_cases.category_update_use_case import (
    category_update_use_case
)
from app.test.ecommerce.utils.sample_data.category_data import (
    category_request
)
from app.core.error.response import ResponseTypes
from app.ecommerce.category.requests.category_request import validate_category_data

from unittest import TestCase




class TestCategoryDeleteseCase(TestCase):
    def setUp(self):
        self.payload = category_request
        self.cat_repo = CategoryRepository()
        self.test_category = self.cat_repo.create_category(category_request)

    def test_update_category_by_invalid_id(self):
        updated_data = {
            "title": "updated_title",
        }
        req = validate_category_data(data=updated_data, id="df")
        res = category_update_use_case(req)
        assert res.type == ResponseTypes.BADREQUEST_ERROR

    def test_update_category_by_id(self):
        updated_data = {
            "title": "updated_title",
        }
        req = validate_category_data(
            data=updated_data,
            id=str(self.test_category.value["data"].id)
        )
        res = category_update_use_case(req)
        assert res.value["data"].title == updated_data["title"]
