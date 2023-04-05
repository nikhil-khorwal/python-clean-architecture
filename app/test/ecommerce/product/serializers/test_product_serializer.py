import copy
import json
from unittest import TestCase
from app.ecommerce.category.domain.category_domain import CategoryDomain
from app.ecommerce.product.domain.product_domain import ProductDomain
from app.ecommerce.product.serializers.product_serializer import ProductSerializer
from app.test.ecommerce.utils.sample_data.product_data import product_response
from app.test.ecommerce.utils.sample_data.category_data import category_response


class TestProductSerializer(TestCase):
    def setUp(self):
        self.payload = product_response

    def test_product_serializer(self):
        category_obj = CategoryDomain(**category_response)
        data = copy.deepcopy(self.payload)
        data.update({"category": category_obj})
        product_obj = ProductDomain(**data)

        expected_json_product = f"""{{
            "id": {data["id"]},
            "title": "{data["title"]}",
            "desc": "{data["desc"]}",
            "images": "{data["images"]}",
            "price": {data["price"]},
            "stock": {data["stock"]},
            "gst_percentage": {data["gst_percentage"]},
            "discount_percentage": {data["discount_percentage"]},
            "category": {{
                "id": {data["category"].id},
                "title": "{data["category"].title}"
            }}
        }}"""
        
        json_product = json.dumps(product_obj, cls=ProductSerializer)
        expected_json = json.loads(expected_json_product)
        expected_json.update({"images" : data["images"]})
        assert json.loads(json_product) == expected_json
