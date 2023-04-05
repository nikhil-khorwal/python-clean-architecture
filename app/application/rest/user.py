import json
from flask import current_app, request, Blueprint, Response
from app.core.methods.core_method import validate_params_id
from app.ecommerce.user.serializers.user_serializer import AdminUserSerializer
from app.core.error.response import STATUS_CODES
from app.ecommerce.user.use_cases.user_delete_use_case import (
    user_delete_use_case)
from app.ecommerce.user.use_cases.user_get_all_users_use_case import (
    user_get_all_users_use_case,)
from app.ecommerce.user.use_cases.user_get_by_id_use_case import (
    user_get_by_id_use_case)
from app.ecommerce.user.use_cases.user_login_use_case import (
    user_login_use_case)
from app.ecommerce.user.use_cases.user_profile_use_case import (
    user_profile_use_case)
from app.ecommerce.user.use_cases.user_signup_use_case import (
    user_signup_use_case)
from app.ecommerce.user.use_cases.user_update_profile_use_case import (
    user_update_use_case,)
from app.core.middleware.user_middleware import (
    token_required, admin_token_required)
from app.ecommerce.user.requests.user_request import (
    validate_user_signin_data,
    validate_user_signup_data,)
from app.ecommerce.user.serializers.user_serializer import UserSerializer


blueprint = Blueprint("user", __name__, url_prefix="/users")


@blueprint.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    request_data = validate_user_signup_data(data)
    res = user_signup_use_case(request=request_data)

    return Response(
        json.dumps(res.value, cls=UserSerializer),
        mimetype="application/json",
        status=STATUS_CODES[res.type],
    )


@blueprint.route("/signup/admin", methods=["POST"])
def signup_admin():
    data = request.get_json()
    request_data = validate_user_signup_data(data)
    res = user_signup_use_case(request=request_data)
    return Response(
        json.dumps(res.value, cls=UserSerializer),
        mimetype="application/json",
        status=STATUS_CODES[res.type],
    )


@blueprint.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    request_data = validate_user_signin_data(data)
    res = user_login_use_case(request=request_data)
    return Response(
        json.dumps(res.value, cls=UserSerializer),
        mimetype="application/json",
        status=STATUS_CODES[res.type],
    )


@blueprint.route("/me", methods=["GET"])
@token_required
def profile():
    res = user_profile_use_case()
    return Response(
        json.dumps(res.value, cls=(UserSerializer)),
        mimetype="application/json",
        status=STATUS_CODES[res.type],
    )


@blueprint.route("/me", methods=["PUT"])
@token_required
def update_profile():
    data = request.get_json()
    res = user_update_use_case(data)
    return Response(
        json.dumps(res.value, cls=(UserSerializer)),
        mimetype="application/json",
        status=STATUS_CODES[res.type],
    )


@blueprint.route("/<user_id>", methods=["PUT"])
@admin_token_required
def update_user(user_id):
    data: dict = request.get_json()
    data["id"] = user_id
    res = user_update_use_case(data)
    return Response(
        json.dumps(res.value, cls=(UserSerializer)),
        mimetype="application/json",
        status=STATUS_CODES[res.type],
    )


@blueprint.route("/", methods=["GET"])
@admin_token_required
def get_all_users():
    res = user_get_all_users_use_case()
    return Response(
        json.dumps(res.value, cls=(AdminUserSerializer)),
        mimetype="application/json",
        status=STATUS_CODES[res.type],
    )


@blueprint.route("/<user_id>", methods=["GET"])
@admin_token_required
def get_user_by_id(user_id):
    request = validate_params_id(user_id)
    res = user_get_by_id_use_case(request)
    return Response(
        json.dumps(res.value, cls=(AdminUserSerializer)),
        mimetype="application/json",
        status=STATUS_CODES[res.type],
    )


@blueprint.route("/<user_id>", methods=["DELETE"])
@admin_token_required
def delete_user(user_id):
    request = validate_params_id(user_id)
    res = user_delete_use_case(request)
    return Response(
        json.dumps(res.value, cls=(AdminUserSerializer)),
        mimetype="application/json",
        status=STATUS_CODES[res.type],
    )
