import pytest
from app.ecommerce.category.repository.category_repository import (
    CategoryRepository
)
from app.ecommerce.product.use_cases.product_create_use_case import (
    product_create_use_case
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




class TestProductCreateUseCase(TestCase):
    def setUp(self):
        self.payload = product_request
        self.cat_repo = CategoryRepository()
        self.test_category = self.cat_repo.create_category(category_request)

    def test_product_create_with_invalid_price(self):
        data = copy.deepcopy(self.payload)
        data["price"] = -2323
        req = validate_product_data(data)
        res = product_create_use_case(req)
        assert res.type == ResponseTypes.BADREQUEST_ERROR

    def test_product_create_with_valid_data(self):
        data = copy.deepcopy(self.payload)
        data.update({"category_id": self.test_category.value["data"].id})
        req = validate_product_data(data)
        res = product_create_use_case(req)

        assert res.type == ResponseTypes.SUCCESS
