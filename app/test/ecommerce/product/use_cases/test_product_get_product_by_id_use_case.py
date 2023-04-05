import pytest
from app.core.methods.core_method import validate_params_id
from app.ecommerce.category.repository.category_repository import (
    CategoryRepository
)
from app.ecommerce.product.use_cases.product_create_use_case import (
    product_create_use_case
)
from app.ecommerce.product.use_cases.product_get_by_id_use_case import (
    product_get_by_id_use_case
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




class TestProductGetByIdUseCase(TestCase):
    def setUp(self):
        self.payload = product_request
        self.cat_repo = CategoryRepository()
        self.test_category = self.cat_repo.create_category(category_request)
        data = copy.deepcopy(self.payload)
        data.update({"category_id": self.test_category.value["data"].id})
        req = validate_product_data(data)
        self.test_product = product_create_use_case(req)

    def test_get_product_by_invalid_id(self):
        req_id = validate_params_id("sad")
        res = product_get_by_id_use_case(req_id)
        assert res.type == ResponseTypes.BADREQUEST_ERROR

    def test_get_product_by_id(self):
        req_id = validate_params_id(self.test_product.value["data"].id)
        res_get_id = product_get_by_id_use_case(req_id)
        assert res_get_id.value.price == self.test_product.value["data"].price
