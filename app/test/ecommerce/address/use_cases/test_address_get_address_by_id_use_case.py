from flask import current_app
import pytest
from app.core.methods.core_method import validate_params_id
from app.ecommerce.address.repository.address_repository import (
    AddressRepository
)
from app.ecommerce.address.use_cases.address_get_by_id_use_case import (
    address_get_by_id_use_case
)
from app.test.ecommerce.utils.sample_data.method import create_address, create_admin_user, create_user
from app.test.ecommerce.utils.sample_data.address_data import (
    address_request
)
from app.core.error.response import ResponseTypes
from unittest import TestCase




class TestAddressGetByIdUseCase(TestCase):

    def setUp(self):
        self.user1 = create_admin_user()
        self.user2 = create_user()
        self.address1 = create_address(user_email=self.user1["email"])

    def test_get_address_by_invalid_id(self):
        with current_app.test_request_context("/?user_email={}".format(self.user1["email"])):
            req_id = validate_params_id("sad")
            res = address_get_by_id_use_case(req_id)
            assert res.type == ResponseTypes.BADREQUEST_ERROR

    def test_get_address_by_id(self):
        with current_app.test_request_context("/?user_email={}".format(self.user1["email"])):
            req_id = validate_params_id(self.address1["id"])
            res_get_id = address_get_by_id_use_case(req_id)
            assert res_get_id.value.pincode == self.address1["pincode"]

    def test_get_address_by_invalid_user_id(self):
        with current_app.test_request_context("/?user_email={}".format(self.user2["email"])):
            req_id = validate_params_id(self.address1["id"])
            res = address_get_by_id_use_case(req_id)
            assert res.type == ResponseTypes.BADREQUEST_ERROR
