import json


class UserSerializer(json.JSONEncoder):
    def default(self, o):
        return {
            "id": o.id,
            "first_name": o.first_name,
            "last_name": o.last_name,
            "email": o.email,
            "phone": o.phone
        }


class AdminUserSerializer(json.JSONEncoder):
    def default(self, o):
        return {
            "id": o.id,
            "first_name": o.first_name,
            "last_name": o.last_name,
            "email": o.email,
            "phone": o.phone,
            "is_admin": o.is_admin,
            "is_delete": o.is_delete,
            "is_active": o.is_active
        }
