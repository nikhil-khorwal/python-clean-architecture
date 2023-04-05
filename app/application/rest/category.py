import json
from flask import Blueprint, Response, request
from app.core.methods.core_method import validate_params_id
from app.core.middleware.user_middleware import admin_token_required
from app.ecommerce.category.requests.category_request import (
    validate_category_data,
    validate_create_category_data,
)
from app.core.error.response import STATUS_CODES
from app.ecommerce.category.use_cases.category_create_use_case import (
    category_create_use_case,
)
from app.ecommerce.category.use_cases.category_delete_use_case import (
    category_delete_use_case,
)
from app.ecommerce.category.use_cases.category_get_all_use_case import (
    category_get_all_use_case,
)
from app.ecommerce.category.use_cases.category_get_by_id_use_case import (
    category_get_by_id_use_case,
)
from app.ecommerce.category.use_cases.category_update_use_case import (
    category_update_use_case,
)
from app.ecommerce.category.serializers.category_serializer import (
    CategorySerializer)

blueprint = Blueprint("category", __name__, url_prefix="/categories")


@blueprint.route("/", methods=["POST"])
@admin_token_required
def create_category():
    data = request.get_json()
    req = validate_create_category_data(data=data)
    res = category_create_use_case(req)
    return Response(
        json.dumps(res.value, cls=CategorySerializer),
        mimetype="application/json",
        status=STATUS_CODES[res.type],
    )


@blueprint.route("/", methods=["GET"])
def get_all_categories():
    res = category_get_all_use_case()
    return Response(
        json.dumps(res.value, cls=CategorySerializer),
        mimetype="application/json",
        status=STATUS_CODES[res.type],
    )


@blueprint.route("/<category_id>", methods=["GET"])
def get_category_by_id(category_id):
    req = validate_params_id(category_id)
    res = category_get_by_id_use_case(req)
    return Response(
        json.dumps(res.value, cls=CategorySerializer),
        mimetype="application/json",
        status=STATUS_CODES[res.type],
    )


@blueprint.route("/<category_id>", methods=["PUT"])
@admin_token_required
def update_category(category_id):
    data = request.get_json()
    req = validate_category_data(data=data, id=category_id)
    res = category_update_use_case(req)
    return Response(
        json.dumps(res.value, cls=CategorySerializer),
        mimetype="application/json",
        status=STATUS_CODES[res.type],
    )


@blueprint.route("/<category_id>", methods=["DELETE"])
@admin_token_required
def delete_category(category_id):
    req = validate_params_id(category_id)
    res = category_delete_use_case(req)
    return Response(
        json.dumps(res.value, cls=CategorySerializer),
        mimetype="application/json",
        status=STATUS_CODES[res.type],
    )
