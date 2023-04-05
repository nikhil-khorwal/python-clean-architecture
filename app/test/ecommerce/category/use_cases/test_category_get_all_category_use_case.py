import pytest
from app.ecommerce.category.repository.category_repository import (
    CategoryRepository
)
from app.ecommerce.category.use_cases.category_get_all_use_case import (
    category_get_all_use_case
)
from app.test.ecommerce.utils.sample_data.category_data import (
    category_request
)
from unittest import TestCase




class TestCategoryGetAllUseCase(TestCase):
    def setUp(self):
        self.payload = category_request
        self.cat_repo = CategoryRepository()
        self.test_category = self.cat_repo.create_category(category_request)

    def test_get_all_categories(self):
        res_get_all = category_get_all_use_case()
        assert len(res_get_all.value) > 0
