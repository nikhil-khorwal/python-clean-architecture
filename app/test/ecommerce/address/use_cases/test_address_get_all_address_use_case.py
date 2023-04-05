from flask import current_app
import pytest
from app.ecommerce.address.repository.address_repository import (
    AddressRepository
)
from app.ecommerce.address.use_cases.address_get_all_use_case import (
    address_get_all_use_case
)
from app.test.ecommerce.utils.sample_data.method import create_address, create_admin_user, create_user
from app.test.ecommerce.utils.sample_data.address_data import (
    address_request
)
from unittest import TestCase




class TestAddressGetAllUseCase(TestCase):
    def setUp(self):
        self.user1 = create_admin_user()
        self.address1 = create_address(user_email=self.user1["email"])

    def test_get_all_address(self):
        with current_app.test_request_context("/?user_email={}".format(self.user1["email"])):
            res_get_all = address_get_all_use_case()
            assert len(res_get_all.value) > 0
