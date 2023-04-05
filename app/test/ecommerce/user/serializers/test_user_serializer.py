import json
from unittest import TestCase
from app.ecommerce.user.serializers.user_serializer import AdminUserSerializer
from app.test.ecommerce.utils.sample_data.email_generator import generate_random_emails

from app.ecommerce.user.domain.user_domain import UserDomain
from app.ecommerce.user.serializers.user_serializer import UserSerializer
from app.test.ecommerce.utils.sample_data.user_data import admin_response


class TestUserSerializer(TestCase):
    def setUp(self):
        self.payload = admin_response

    def test_user_serializer(self):
        user = UserDomain(**self.payload)

        expected_json_user = {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "phone": user.phone
        }

        json_user = json.dumps(user, cls=UserSerializer)
        assert json.loads(json_user) == expected_json_user
