import pytest
from app.ecommerce.user.use_cases.user_login_use_case import (
    user_login_use_case
)
from app.ecommerce.user.repository.user_repository import UserRepository
from app.test.ecommerce.utils.sample_data.email_generator import generate_random_emails
from app.core.error.response import ResponseTypes
from app.ecommerce.user.requests.user_request import validate_user_signin_data, validate_user_signup_data

import copy
from unittest import TestCase
from app.test.ecommerce.utils.sample_data.method import create_admin_user, create_user
from app.test.ecommerce.utils.sample_data.user_data import admin_request


class TestUserLoginUseCase(TestCase):
    def setUp(self):
        self.payload = admin_request
        self.repo = UserRepository()
        self.user = create_admin_user()

    def test_user_login_with_invalid_email_format(self):
        data = copy.deepcopy(self.payload)
        data.update({"email":data['email'].replace('@', '')})
        req = validate_user_signin_data(data)
        res = user_login_use_case(req)
        assert res.type == ResponseTypes.BADREQUEST_ERROR

    def test_user_login_with_valid_data(self):
        req = validate_user_signin_data(self.payload)
        res = user_login_use_case(req)
        assert res.value["data"].email == self.payload['email']
        assert res.value["data"].phone == self.payload['phone']
        assert "token" in res.value
