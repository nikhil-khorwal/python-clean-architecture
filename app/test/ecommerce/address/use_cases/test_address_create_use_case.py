from flask import current_app
import pytest

from app.ecommerce.address.repository.address_repository import AddressRepository
from app.ecommerce.address.use_cases.address_create_use_case import (
    address_create_use_case,
)
from app.test.ecommerce.utils.sample_data.email_generator import generate_random_emails
from app.test.ecommerce.utils.sample_data.method import create_address, create_user
from app.test.ecommerce.utils.sample_data.address_data import address_request
from app.core.error.response import ResponseTypes
from app.ecommerce.address.requests.address_request import validate_create_address_data
from app.ecommerce.user.repository.user_repository import UserRepository
from app.test.ecommerce.utils.sample_data.user_data import test_user_request

import copy
from unittest import TestCase




class TestAddressCreateUseCase(TestCase):
    def setUp(self):
        self.payload = address_request
        self.user1 = create_user()

    def test_address_create_with_invalid_pincode(self):
        with current_app.test_request_context(
            "/?user_email={}".format(self.user1["email"])
        ):
            data = copy.deepcopy(self.payload)
            data["pincode"] = -1
            req = validate_create_address_data(data)
            res = address_create_use_case(req)
            assert res.type == ResponseTypes.BADREQUEST_ERROR

    def test_address_create_with_valid_data(self):
        with current_app.test_request_context(
            "/?user_email={}".format(self.user1["email"])
        ):
            data = copy.deepcopy(self.payload)
            req = validate_create_address_data(data)
            res = address_create_use_case(req)
            assert res.type == ResponseTypes.SUCCESS
