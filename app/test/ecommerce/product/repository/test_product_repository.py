
import copy
from unicodedata import category
from unittest import TestCase
import pytest
from app.ecommerce.product.repository.product_repository import ProductRepository
from app.ecommerce.category.repository.category_repository import (
    CategoryRepository
)
from app.test.ecommerce.utils.sample_data.method import create_category, create_product
from app.test.ecommerce.utils.sample_data.category_data import (
    category_request
)
from app.test.ecommerce.utils.sample_data.product_data import (
    product_request
)


class TestProductRepository(TestCase):
    def setUp(self):
        self.repository = ProductRepository()
        self.payload = product_request
        self.category = create_category()
        self.product = create_product(self.category["id"])

    def test_create_product_success(self):
        data = copy.deepcopy(self.payload)
        data.update({"category_id": self.category["id"]})
        new_product = self.repository.create_product(data)
        assert new_product.value["data"].title == data['title']
        assert new_product.value["data"].price == data['price']

    def test_get_all_product(self):
        all_product = self.repository.get_all_products()
        self.assertGreater(len(all_product.value), 0)

    def test_get_product_by_id(self):
        product = self.repository.get_product_by_id(
            self.product["id"]
        )
        self.assertEqual(self.payload["title"], product.value.title)

    def test_update_product(self):
        data = {
            "title": "update_title",
            "id": self.product["id"]
        }
        product = self.repository.update_product(data)
        self.assertEqual(product.value["data"].title, data["title"])

    def test_delete_product(self):
        product = self.repository.delete_product(self.product["id"])
        self.assertEqual(
            product.value["message"],
            "delete product successfully"
        )