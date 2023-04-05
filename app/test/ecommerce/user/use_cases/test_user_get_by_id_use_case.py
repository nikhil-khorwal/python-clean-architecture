import pytest
from app.ecommerce.user.use_cases.user_get_by_id_use_case import (
    user_get_by_id_use_case
)
from app.ecommerce.user.repository.user_repository import UserRepository
from app.core.methods.core_method import validate_params_id
from app.test.ecommerce.utils.sample_data.email_generator import generate_random_emails
from app.core.error.response import ResponseTypes
from unittest import TestCase
from app.test.ecommerce.utils.sample_data.method import create_admin_user, create_user
from app.test.ecommerce.utils.sample_data.user_data import admin_request



class TestUserGetUserByIdUseCase(TestCase):
    def setUp(self):
        self.payload = admin_request
        self.repo = UserRepository()
        self.user = create_admin_user()


    def test_user_get_users_by_id_use_case(self):
        req = validate_params_id(self.user["id"])
        res = user_get_by_id_use_case(req)
        assert res.type == ResponseTypes.SUCCESS
