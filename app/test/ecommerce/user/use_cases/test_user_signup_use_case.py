import copy
from app.ecommerce.user.use_cases.user_signup_use_case import (
        user_signup_use_case
)
from app.test.ecommerce.utils.sample_data.email_generator import generate_random_emails
from unittest import TestCase
import pytest
from app.core.error.response import ResponseTypes
from app.ecommerce.user.repository.user_repository import UserRepository
from app.ecommerce.user.requests.user_request import validate_user_signup_data
from app.test.ecommerce.utils.sample_data.method import create_admin_user, create_user
from app.test.ecommerce.utils.sample_data.user_data import admin_request


class TestUserLoginUseCase(TestCase):
    def setUp(self):
        self.payload = admin_request
        self.repo = UserRepository()
        self.user = create_admin_user()

    def test_user_signup_with_invalid_email_format(self):
        data = copy.deepcopy(self.payload)
        data.update({"email":data['email'].replace('@', '')})
        req = validate_user_signup_data(self.payload)
        res = user_signup_use_case(req)
        assert res.type == ResponseTypes.BADREQUEST_ERROR

    def test_user_signup_with_valid_data(self):
        data = copy.deepcopy(self.payload)
        data.update({"email":generate_random_emails()})
        req = validate_user_signup_data(data)
        res = user_signup_use_case(req)
        assert res.type == ResponseTypes.SUCCESS
        assert res.value["data"].email == data["email"]
