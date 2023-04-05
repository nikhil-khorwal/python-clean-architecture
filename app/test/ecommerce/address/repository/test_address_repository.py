import copy
from unittest import TestCase
from flask import current_app
import pytest
from app.ecommerce.address.repository.address_repository import AddressRepository
from app.test.ecommerce.utils.sample_data.method import create_address, create_admin_user
from app.test.ecommerce.utils.sample_data.address_data import address_request



class TestAddressRepository(TestCase):
    def setUp(self):
        self.payload = address_request
        self.user1 = create_admin_user()
        self.address1 = create_address(user_email=self.user1["email"])
        self.repository = AddressRepository()

    def test_create_address(self):
        with current_app.test_request_context("/?user_email={}".format(self.user1["email"])):
            data = copy.deepcopy(self.payload)
            address = self.repository.create_address(data)
            res = address.value["data"].to_dict()
            res.pop("id")
            assert res == data

    def test_get_all_address(self):
        all_address = self.repository.get_all_addresses()
        self.assertGreater(len(all_address.value), 0)

    def test_get_all_user_address(self):
        with current_app.test_request_context("/?user_email={}".format(self.user1["email"])):
            all_address = self.repository.get_all_user_addresses()
            self.assertGreater(len(all_address.value), 0)

    def test_get_address_by_id(self):
        with current_app.test_request_context("/?user_email={}".format(self.user1["email"])):
            address = self.repository.get_address_by_id(self.address1["id"])
            self.assertEqual(self.address1["street"], address.value.street)

    def test_update_address(self):
        with current_app.test_request_context("/?user_email={}".format(self.user1["email"])):
            data = {
                "street": "update_street",
                "id": self.address1["id"]
            }
            address = self.repository.update_address(data)
            self.assertEqual(address.value["data"].street, data["street"])

    def test_delete_address(self):
        with current_app.test_request_context("/?user_email={}".format(self.user1["email"])):
            address = self.repository.delete_address(self.address1["id"])
            self.assertEqual(
                address.value["message"],
                "delete address successfully"
            )   
