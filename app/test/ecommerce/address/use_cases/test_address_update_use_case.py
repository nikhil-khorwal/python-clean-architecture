from flask import current_app
import pytest
from app.ecommerce.address.repository.address_repository import (
    AddressRepository
)
from app.ecommerce.address.use_cases.address_update_use_case import (
    address_update_use_case
)
from app.test.ecommerce.utils.sample_data.method import create_address, create_admin_user, create_user
from app.test.ecommerce.utils.sample_data.address_data import (
    address_request
)
from app.core.error.response import ResponseTypes
from app.ecommerce.address.requests.address_request import validate_address_data

from unittest import TestCase




class TestAddressUpdateUseCase(TestCase):

    def setUp(self):
        self.user1 = create_admin_user()
        self.user2 = create_user()
        self.address1 = create_address(user_email=self.user1["email"])

    def test_update_address_by_invalid_id(self):
        updated_data = {
            "street": "updated_street",
        }
        req = validate_address_data(data=updated_data, id="df")
        res = address_update_use_case(req)
        assert res.type == ResponseTypes.BADREQUEST_ERROR

    def test_update_address_by_id(self):
        with current_app.test_request_context("/?user_email={}".format(self.user1["email"])):
            updated_data = {
                "street": "updated_street",
            }
            req = validate_address_data(
                data=updated_data,
                id=self.address1["id"]
            )
            res = address_update_use_case(req)
            assert res.value["data"].street == updated_data["street"]

    def test_delete_address_by_invalid_user_id(self):
        with current_app.test_request_context("/?user_email={}".format(self.user2["email"])):
            updated_data = {
                "street": "updated_street",
            }
            req = validate_address_data(    
                data=updated_data,
                id=self.address1["id"]
            )
            res = address_update_use_case(req)
            assert res.type == ResponseTypes.BADREQUEST_ERROR