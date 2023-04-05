import copy
from unittest import TestCase
from app.test.ecommerce.utils.sample_data.address_data import address_response
from app.ecommerce.address.domain.address_domain import AddressDomain


class TestAddressDomain(TestCase):
    def setUp(self):
        self.payload = address_response

    def test_address_domain(self):
        demo_address = AddressDomain(**self.payload)
        self.assertEqual(demo_address.pincode, self.payload["pincode"])

    def test_address_from_dict(self):
        demo_address = AddressDomain.from_dict(self.payload)
        self.assertEqual(demo_address.pincode, self.payload["pincode"])

    def test_address_to_dict(self):
        demo_address = AddressDomain.from_dict(self.payload)
        data = copy.deepcopy(self.payload)
        self.assertEqual(demo_address.to_dict(), data)
