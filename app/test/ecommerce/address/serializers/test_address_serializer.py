import json
from unittest import TestCase
from app.ecommerce.address.domain.address_domain import AddressDomain
from app.ecommerce.address.serializers.address_serializer import (
    AddressSerializer
)
from app.test.ecommerce.utils.sample_data.address_data import address_response


class TestAddressSerializer(TestCase):
    def setUp(self):
        self.payload = address_response

    def test_address_serializer(self):
        address_obj = AddressDomain(**address_response)

        expected_json_address = f"""{{
            "id": {self.payload["id"]},
            "house_no": "{self.payload["house_no"]}",
            "street": "{self.payload["street"]}",
            "landmark": "{self.payload["landmark"]}",
            "pincode": {self.payload["pincode"]},
            "city": "{self.payload["city"]}",
            "state": "{self.payload["state"]}"
        }}"""

        json_address = json.dumps(address_obj, cls=AddressSerializer)
        assert json.loads(json_address) == json.loads(expected_json_address)
