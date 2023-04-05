import pytest
from app.ecommerce.category.repository.category_repository import (
    CategoryRepository
)
from app.ecommerce.product.use_cases.product_create_use_case import (
    product_create_use_case
)
from app.ecommerce.product.use_cases.product_update_use_case import (
    product_update_use_case
)
from app.test.ecommerce.utils.sample_data.category_data import (
    category_request
)
from app.core.error.response import ResponseTypes
from app.ecommerce.product.requests.product_request import validate_product_data
from app.test.ecommerce.utils.sample_data.product_data import (
    product_request
)

import copy
from unittest import TestCase




class TestProductDeleteseCase(TestCase):
    def setUp(self):
        self.payload = product_request
        self.cat_repo = CategoryRepository()
        self.test_category = self.cat_repo.create_category(category_request)
        data = copy.deepcopy(self.payload)
        data.update({"category_id": self.test_category.value["data"].id})
        req = validate_product_data(data)
        self.test_product = product_create_use_case(req)

    def test_update_product_by_invalid_id(self):
        updated_data = {
            "price": 1244,
        }
        req = validate_product_data(data=updated_data, id="df")
        res = product_update_use_case(req)
        assert res.type == ResponseTypes.BADREQUEST_ERROR

    def test_update_product_by_id(self):
        updated_data = {
            "price": 1244,
        }
        req = validate_product_data(
            data=updated_data,
            id=str(self.test_product.value["data"].id)
        )
        res = product_update_use_case(req)
        assert res.value["data"].price == updated_data["price"]
