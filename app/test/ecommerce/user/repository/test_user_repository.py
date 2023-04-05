import copy
from unittest import TestCase
import pytest
from app.test.ecommerce.utils.sample_data.email_generator import generate_random_emails
from app.core.error.response import ResponseTypes
from app.ecommerce.user.repository.user_repository import UserRepository
from app.test.ecommerce.utils.sample_data.method import create_admin_user, create_user
from app.test.ecommerce.utils.sample_data.user_data import admin_request



class TestUserRepository(TestCase):
    def setUp(self):
        self.payload = admin_request
        self.repo = UserRepository()
        self.user = create_admin_user()

    def test_create_user_success(self):
        data = copy.deepcopy(self.payload)
        new_user = self.repo.user_sign_up(data)
        assert new_user.value["data"].email == data['email']
        assert new_user.value["data"].phone == data['phone']

    def test_user_with_email_exist_error(self):
        data = copy.deepcopy(self.payload)
        data.update({"email":self.user["email"]})
        new_user = self.repo.user_sign_up(data)
        assert new_user.type == ResponseTypes.BADREQUEST_ERROR

    def test_login_with_valid_credentials(self):
        new_user = self.repo.user_login(self.payload)
        assert new_user.value["data"].email == self.payload['email']
        assert new_user.value["data"].phone == self.payload['phone']
        assert "token" in new_user.value

    def test_login_with_invalid_email_credentials(self):
        data = copy.deepcopy(self.payload)
        data.update({"email":generate_random_emails()})
        new_user = self.repo.user_login(data)
        assert "token" not in new_user.value
        assert new_user.type == ResponseTypes.BADREQUEST_ERROR

    def test_login_with_valid_email_invalid_password_credentials(self):
        data = copy.deepcopy(self.payload)
        data.update({"password":"sdsdsd"})
        new_user = self.repo.user_login(data)
        assert "token" not in new_user.value
        assert new_user.type == ResponseTypes.BADREQUEST_ERROR

    def test_get_users_by_id(self):
        res = self.repo.user_get_by_id(
            self.user["id"]
        )
        assert res.type == ResponseTypes.SUCCESS
        assert res.value.email == self.user["email"]

    def test_user_delete_with_valid_id_not_found(self):
        random_id = 2564252
        res = self.repo.user_delete(random_id)
        assert res.type == ResponseTypes.SUCCESS

    def test_user_delete(self):
        res = self.repo.user_delete(self.user["id"])
        assert res.type == ResponseTypes.SUCCESS
        assert res.value["message"] == "Delete user successfully"
