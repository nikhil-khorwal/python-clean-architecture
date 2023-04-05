import pytest
from app.ecommerce.category.repository.category_repository import (
    CategoryRepository
)
from app.ecommerce.product.use_cases.product_create_use_case import (
    product_create_use_case
)
from app.ecommerce.product.use_cases.product_get_all_use_case import (
    product_get_all_use_case
)
from app.test.ecommerce.utils.sample_data.category_data import (
    category_request
)
from app.ecommerce.product.requests.product_request import validate_product_data
from app.test.ecommerce.utils.sample_data.product_data import (
    product_request
)

import copy
from unittest import TestCase




class TestProductGetAllUseCase(TestCase):
    def setUp(self):
        self.payload = product_request
        self.cat_repo = CategoryRepository()
        self.test_category = self.cat_repo.create_category(category_request)

    def test_get_all_products(self):
        data = copy.deepcopy(self.payload)
        data.update({"category_id": self.test_category.value["data"].id})
        req = validate_product_data(data)
        product_create_use_case(req)
        res_get_all = product_get_all_use_case()

        assert len(res_get_all.value) > 0
