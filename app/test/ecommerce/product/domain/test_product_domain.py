import copy
from unittest import TestCase
from app.test.ecommerce.utils.sample_data.product_data import product_response
from app.ecommerce.product.domain.product_domain import ProductDomain


class TestProductDomain(TestCase):
    def setUp(self):
        self.payload = product_response

    def test_product_domain(self):
        demo_product = ProductDomain(**self.payload)
        self.assertEqual(demo_product.title, self.payload["title"])
        self.assertEqual(demo_product.price, self.payload["price"])

    def test_product_from_dict(self):
        demo_product = ProductDomain.from_dict(self.payload)
        self.assertEqual(demo_product.title, self.payload["title"])
        self.assertEqual(demo_product.price, self.payload["price"])

    def test_product_to_dict(self):
        demo_product = ProductDomain.from_dict(self.payload)
        data = copy.deepcopy(self.payload)
        self.assertEqual(demo_product.to_dict(), data)
