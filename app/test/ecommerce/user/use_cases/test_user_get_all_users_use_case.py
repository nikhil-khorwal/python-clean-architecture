import pytest
from app.ecommerce.user.use_cases.user_get_all_users_use_case import (
    user_get_all_users_use_case
)
from app.ecommerce.user.repository.user_repository import UserRepository
from app.test.ecommerce.utils.sample_data.email_generator import generate_random_emails
from app.core.error.response import ResponseTypes
from unittest import TestCase
from app.test.ecommerce.utils.sample_data.method import create_admin_user, create_user
from app.test.ecommerce.utils.sample_data.user_data import admin_request



class TestUserGetAllUseCase(TestCase):

    def test_user_get_all_users_use_case(self):
        res = user_get_all_users_use_case()
        assert res.type == ResponseTypes.SUCCESS
        assert len(res.value) > 0
