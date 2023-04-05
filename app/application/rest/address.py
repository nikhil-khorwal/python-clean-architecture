import json
from flask import Blueprint, Response, request
from app.core.methods.core_method import validate_params_id
from app.core.middleware.user_middleware import (
    admin_token_required,
    token_required
)
from app.ecommerce.address.requests.address_request import (
    validate_address_data,
    validate_create_address_data,
)
from app.core.error.response import STATUS_CODES
from app.ecommerce.address.use_cases.address_create_use_case import (
    address_create_use_case,
)
from app.ecommerce.address.use_cases.address_delete_use_case import (
    address_delete_use_case,
)
from app.ecommerce.address.use_cases.address_get_all_for_user_use_case import (
    address_get_all_for_user_use_case,
)
from app.ecommerce.address.use_cases.address_get_all_use_case import (
    address_get_all_use_case,
)
from app.ecommerce.address.use_cases.address_get_by_id_use_case import (
    address_get_by_id_use_case,
)
from app.ecommerce.address.use_cases.address_update_use_case import (
    address_update_use_case,
)
from app.ecommerce.address.serializers.address_serializer import (
    AddressSerializer
)

blueprint = Blueprint("address", __name__, url_prefix="/address")


@blueprint.route("/", methods=["POST"])
@token_required
def create_address():
    data = request.get_json()
    req = validate_create_address_data(data=data)
    res = address_create_use_case(req)
    return Response(
        json.dumps(res.value, cls=AddressSerializer),
        mimetype="application/json",
        status=STATUS_CODES[res.type],
    )


@blueprint.route("/", methods=["GET"])
@admin_token_required
def get_all_addresss():
    res = address_get_all_use_case()
    return Response(
        json.dumps(res.value, cls=AddressSerializer),
        mimetype="application/json",
        status=STATUS_CODES[res.type],
    )


@blueprint.route("/me", methods=["GET"])
@token_required
def get_all_user_addresss():
    res = address_get_all_for_user_use_case()
    return Response(
        json.dumps(res.value, cls=AddressSerializer),
        mimetype="application/json",
        status=STATUS_CODES[res.type],
    )


@blueprint.route("/<address_id>", methods=["GET"])
@token_required
def get_address_by_id(address_id):
    req = validate_params_id(address_id)
    res = address_get_by_id_use_case(req)
    return Response(
        json.dumps(res.value, cls=AddressSerializer),
        mimetype="application/json",
        status=STATUS_CODES[res.type],
    )


@blueprint.route("/<address_id>", methods=["PUT"])
@token_required
def update_address(address_id):
    data = request.get_json()
    req = validate_address_data(data=data, id=address_id)
    res = address_update_use_case(req)
    return Response(
        json.dumps(res.value, cls=AddressSerializer),
        mimetype="application/json",
        status=STATUS_CODES[res.type],
    )


@blueprint.route("/<address_id>", methods=["DELETE"])
@token_required
def delete_address(address_id):
    req = validate_params_id(address_id)
    res = address_delete_use_case(req)
    return Response(
        json.dumps(res.value, cls=AddressSerializer),
        mimetype="application/json",
        status=STATUS_CODES[res.type],
    )
