import copy
import json
from unittest import TestCase, mock

import pytest
from app.ecommerce.user.serializers.user_serializer import AdminUserSerializer
from app.ecommerce.user.repository.user_repository import UserRepository
from app.test.ecommerce.utils.sample_data.email_generator import generate_random_emails
from app.core.error.response import ResponseSuccess
from app.test.ecommerce.utils.sample_data.rest_responses import (
    login_response,
    delete_response,
    update_response,
    user_response
)

test_email_rest = generate_random_emails()
payload_rest = {
    "first_name": "test",
    "last_name": "test",
    "email": test_email_rest,
    "password": "test123",
    "phone": "0123456789",
    "is_admin": True,
    "is_active": True,
    "is_delete": False,
    "created_at": "2022-10-14 17:19:22.204637",
    "updated_at": "2022-10-14 17:19:22.204666"
}
rest_repo = UserRepository()
test_signup_user_rest = rest_repo.user_sign_up(payload_rest)


class TestUserRestApi(TestCase):

    @pytest.fixture(autouse=True)
    def set_up_fixture(self, client):
        self.client = client

    @mock.patch("app.application.rest.user.user_signup_use_case")
    def test_signup(self, mock_use_case):
        user = copy.deepcopy(payload_rest)
        mock_use_case.return_value = ResponseSuccess([payload_rest])
        res = self.client.post("/users/signup", json=user)
        user.pop("password")
        assert json.loads(res.data.decode("UTF-8"))[0]["email"] == user["email"]
        assert res.status_code == 200
        assert res.mimetype == "application/json"


    @mock.patch("app.application.rest.user.user_login_use_case")
    def test_login(self, mock_use_case):
        mock_use_case.return_value = ResponseSuccess(login_response)
        res = self.client.post("/users/login", json=payload_rest)
        assert "token" in json.loads(res.data.decode("UTF-8"))
        assert res.status_code == 200


    @mock.patch("app.application.rest.user.user_profile_use_case")
    def test_get_user_profile(self, mock_use_case):
        user = copy.deepcopy(payload_rest)
        mock_use_case.return_value = ResponseSuccess(login_response)
        login_res = self.client.post("/users/login", json=user)
        res_data = json.loads(login_res.data.decode("UTF-8"))
        token = res_data["token"]
        user.pop("password")
        mock_use_case.return_value = ResponseSuccess([user])
        res = self.client.get("/users/me", headers={"Authorization": token})
        assert json.loads(res.data.decode("UTF-8")) == [user]
        assert res.status_code == 200


    @mock.patch("app.application.rest.user.user_update_use_case")
    def test_update_user_profile(self, mock_use_case):
        user = copy.deepcopy(payload_rest)
        mock_use_case.return_value = ResponseSuccess(login_response)
        login_res = self.client.post("/users/login", json=user)
        res_data = json.loads(login_res.data.decode("UTF-8"))
        token = res_data["token"]
        updated_data = {
            "first_name": "updated_name"
        }
        user.update(updated_data)
        update_response["data"] = json.loads(
            login_res.data.decode("UTF-8")
        )["data"]
        mock_use_case.return_value = ResponseSuccess(updated_data)
        res = self.client.put("/users/me", headers={
            "Authorization": token
        }, json=updated_data)
        assert json.loads(res.data.decode("UTF-8"))["first_name"] == "updated_name"
        assert res.status_code == 200


    @mock.patch("app.application.rest.user.user_get_all_users_use_case")
    def test_get_all_users(self, mock_use_case):
        user = copy.deepcopy(payload_rest)
        mock_use_case.return_value = ResponseSuccess(login_response)
        login_res = self.client.post("/users/login", json=user)
        res_data = json.loads(login_res.data.decode("UTF-8"))
        token = res_data["token"]
        mock_use_case.return_value = ResponseSuccess([user_response])
        res = self.client.get("/users/", headers={
            "Authorization": token
        })
        assert res.status_code == 200


    @mock.patch("app.application.rest.user.user_get_by_id_use_case")
    def test_user_get_by_id(self, mock_use_case):
        user = copy.deepcopy(payload_rest)
        mock_use_case.return_value = ResponseSuccess(login_response)
        login_res = self.client.post("/users/login", json=user)
        res_data = json.loads(login_res.data.decode("UTF-8"))
        token = res_data["token"]

        mock_use_case.return_value = ResponseSuccess(test_signup_user_rest.value)
        res = self.client.get(f"/users/{test_signup_user_rest.value['data'].id}",
                        headers={"Authorization": token})
        user = copy.deepcopy(test_signup_user_rest.value)
        jsondata = json.dumps(user, cls=AdminUserSerializer)
        assert json.loads(res.data.decode("UTF-8")) == json.loads(jsondata)
        assert res.status_code == 200


    @mock.patch("app.application.rest.user.user_delete_use_case")
    def test_delete_user(self, mock_use_case):
        user = copy.deepcopy(payload_rest)
        mock_use_case.return_value = ResponseSuccess(login_response)
        login_res = self.client.post("/users/login", json=user)
        res_data = json.loads(login_res.data.decode("UTF-8"))
        token = res_data["token"]

        mock_use_case.return_value = ResponseSuccess(delete_response)
        res = self.client.delete(f"/users/{test_signup_user_rest.value['data'].id}",
                            headers={"Authorization": token})
        assert res.status_code == 200
