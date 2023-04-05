import copy
from unittest import TestCase
import pytest
from app.ecommerce.user.requests.user_request import (
    validate_user_signup_data
)
from app.core.methods.core_method import validate_params_id
from app.ecommerce.user.repository.user_repository import UserRepository
from app.test.ecommerce.utils.sample_data.user_data import admin_request


class TestUserRequest(TestCase):
    def setUp(self):
        self.payload = admin_request
        self.repo = UserRepository()
        self.test_signup_user = self.repo.user_sign_up(self.payload)

    def test_validate_signup_invalid_email(self):
        data = copy.deepcopy(self.payload)
        data.update({"email":data['email'].replace('@', '')})
        req = validate_user_signup_data(data)
        assert req.has_errors()

    def test_validate_signup_valid_email(self):
        req = validate_user_signup_data(self.payload)
        assert req

    def test_validate_id_invalid_params(self):
        id = "sd"
        req = validate_params_id(id)
        assert req.has_errors()

    def test_validate_id_valid_params(self):
        id = 1
        req = validate_params_id(id)
        assert req
