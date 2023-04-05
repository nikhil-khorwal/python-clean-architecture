import json
from flask import Blueprint, Response, request
from app.core.methods.core_method import validate_params_id
from app.ecommerce.cart.requests.cart_create_request_check import (
    validate_cart_create_data,
    validate_cart_update_data)
from app.ecommerce.cart.use_cases.update_quantity_of_cart_use_case import (
    update_quantity_of_cart_use_case)
from app.ecommerce.cart.use_cases.remove_product_from_cart_use_case import (
    remove_product_from_cart_use_case)
from app.ecommerce.cart.use_cases.get_user_cart_use_case import (
    get_user_cart_use_case)
from app.ecommerce.cart.serializers.cart_serializer import (
    CartAdminSerializer,
    CartSerializer)
from app.ecommerce.cart.use_cases.add_product_to_cart_use_case import (
    add_product_to_cart_use_case)
from app.ecommerce.cart.use_cases.get_all_carts_use_case import (
    get_all_carts_use_case)
from app.ecommerce.cart.use_cases.get_cart_by_id_use_Case import (
    get_cart_by_id_use_case)
from app.core.middleware.user_middleware import (
    token_required, admin_token_required)
from app.core.error.response import STATUS_CODES

blueprint = Blueprint("cart", __name__, url_prefix="/carts")


@blueprint.route("/", methods=["POST"])
@token_required
def add_product_to_cart():
    data = request.get_json()
    req = validate_cart_create_data(data)
    res = add_product_to_cart_use_case(req)
    return Response(
        json.dumps(res.value),
        mimetype="application/json",
        status=STATUS_CODES[res.type],
    )


@blueprint.route("/me", methods=["GET"])
@token_required
def get_user_cart():
    res = get_user_cart_use_case()
    return Response(
        json.dumps(res.value, cls=CartSerializer),
        mimetype="application/json",
        status=STATUS_CODES[res.type],
    )


@blueprint.route("/<cart_item_id>", methods=["DELETE"])
@token_required
def remove_product_from_cart(cart_item_id):
    req = validate_params_id(cart_item_id)
    res = remove_product_from_cart_use_case(req)
    return Response(
        json.dumps(res.value, cls=CartSerializer),
        mimetype="application/json",
        status=STATUS_CODES[res.type],
    )


@blueprint.route("/<cart_item_id>", methods=["PUT"])
@token_required
def update_quantity_of_cart(cart_item_id):
    data = request.get_json()
    req = validate_cart_update_data(data, cart_item_id)
    res = update_quantity_of_cart_use_case(req)
    return Response(
        json.dumps(res.value, cls=CartSerializer),
        mimetype="application/json",
        status=STATUS_CODES[res.type],
    )


@blueprint.route("/<cart_id>", methods=["GET"])
@admin_token_required
def get_cart_by_id(cart_id):
    req = validate_params_id(cart_id)
    res = get_cart_by_id_use_case(req)
    return Response(
        json.dumps(res.value, cls=CartAdminSerializer),
        mimetype="application/json",
        status=STATUS_CODES[res.type],
    )


@blueprint.route("/", methods=["GET"])
@admin_token_required
def get_all_carts():
    res = get_all_carts_use_case()
    return Response(
        json.dumps(res.value, cls=CartAdminSerializer),
        mimetype="application/json",
        status=STATUS_CODES[res.type],
    )
