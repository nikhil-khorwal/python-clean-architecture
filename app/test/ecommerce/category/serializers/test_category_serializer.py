import json
from unittest import TestCase
from app.ecommerce.category.domain.category_domain import CategoryDomain
from app.ecommerce.category.serializers.category_serializer import (
    CategorySerializer
)
from app.test.ecommerce.utils.sample_data.category_data import category_response


class TestcategorySerializer(TestCase):
    def setUp(self):
        self.payload = category_response

    def test_category_serializer(self):
        category_obj = CategoryDomain(**category_response)

        expected_json_category = f"""{{
            "id": {self.payload["id"]},
            "title": "{self.payload["title"]}"
        }}"""

        json_category = json.dumps(category_obj, cls=CategorySerializer)
        assert json.loads(json_category) == json.loads(expected_json_category)
