import copy
from unittest import TestCase
import pytest
from app.test.ecommerce.utils.sample_data.email_generator import generate_random_emails
from app.ecommerce.user.domain.user_domain import UserDomain
from app.test.ecommerce.utils.sample_data.user_data import admin_response

class TestUserDomain(TestCase):
    def setUp(self):
        self.payload = admin_response

    def test_user_domain(self):
        demo_user = UserDomain(**self.payload)
        assert demo_user.email == self.payload["email"]
        assert demo_user.phone == self.payload["phone"]

    def test_user_from_dict(self):
        demo_user = UserDomain.from_dict(self.payload)
        assert demo_user.email == self.payload["email"]
        assert demo_user.phone == self.payload["phone"]

    def test_user_to_dict(self):
        demo_user = UserDomain.from_dict(self.payload)
        data = copy.deepcopy(self.payload)
        assert demo_user.to_dict() == data
