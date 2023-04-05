import json


class AddressSerializer(json.JSONEncoder):
    def default(self, o):
        return {
            "id":o.id,
            "house_no":o.house_no,
            "street":o.street,
            "landmark":o.landmark,
            "pincode":o.pincode,
            "city":o.city,
            "state":o.state
        }
