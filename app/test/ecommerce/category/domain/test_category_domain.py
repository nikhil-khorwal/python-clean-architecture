import copy
from unittest import TestCase
from app.test.ecommerce.utils.sample_data.category_data import category_response
from app.ecommerce.category.domain.category_domain import CategoryDomain


class TestCategoryDomain(TestCase):
    def setUp(self):
        self.payload = category_response

    def test_category_domain(self):
        demo_category = CategoryDomain(**self.payload)
        self.assertEqual(demo_category.title, self.payload["title"])

    def test_category_from_dict(self):
        demo_category = CategoryDomain.from_dict(self.payload)
        self.assertEqual(demo_category.title, self.payload["title"])

    def test_category_to_dict(self):
        demo_category = CategoryDomain.from_dict(self.payload)
        data = copy.deepcopy(self.payload)
        self.assertEqual(demo_category.to_dict(), data)
