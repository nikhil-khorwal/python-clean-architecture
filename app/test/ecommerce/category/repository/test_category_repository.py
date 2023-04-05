
import copy
from unittest import TestCase
import pytest
from app.ecommerce.category.repository.category_repository import (
    CategoryRepository
)
from app.test.ecommerce.utils.sample_data.category_data import (
    category_request
)




class TestcategoryRepository(TestCase):
    def setUp(self):
        self.payload = category_request
        self.repo = CategoryRepository()
        self.cat_repo = CategoryRepository()
        self.test_category = self.cat_repo.create_category(category_request)

    def test_create_category_success(self):
        data = copy.deepcopy(self.payload)
        new_category = self.repo.create_category(data)
        assert new_category.value["data"].title == data['title']

    def test_get_all_category(self):
        all_category = self.repo.get_all_categories()
        self.assertGreater(len(all_category.value), 0)

    def test_get_category_by_id(self):
        category = self.repo.get_category_by_id(
            self.test_category.value["data"].id
        )
        self.assertEqual(self.payload["title"], category.value.title)

    def test_update_category(self):
        data = {
            "title": "update_title",
            "id": self.test_category.value["data"].id
        }
        category = self.repo.update_category(data)
        self.assertEqual(category.value["data"].title, data["title"])

    def test_delete_category(self):
        category = self.repo.delete_category(
            self.test_category.value["data"].id
        )
        self.assertEqual(
            category.value["message"],
            "delete category successfully"
        )
