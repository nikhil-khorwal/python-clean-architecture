import json
from app.core.methods.core_method import validate_params_id
from app.ecommerce.order.serializers.order_serializer import OrderSerializer
from app.ecommerce.order.use_cases.cancle_order_use_case import (
    cancle_order_use_case)
from app.ecommerce.order.use_cases.create_cart_order_use_case import (
    create_cart_order_use_case)
from app.ecommerce.order.use_cases.create_product_order_use_case import (
    create_product_order_use_case)
from flask import Blueprint, Response, request
from app.core.error.response import STATUS_CODES
from app.ecommerce.order.requests.order_request import (
    validate_order_create_data)
from app.core.middleware.user_middleware import (
    token_required,
    admin_token_required
)
from app.ecommerce.order.use_cases.cart_order_detail_use_case import (
    cart_order_detail_use_case
)
from app.ecommerce.order.use_cases.delete_order_use_case import (
    delete_order_use_case
)
from app.ecommerce.order.use_cases.get_all_order_of_user_use_case import (
    get_all_order_of_user_use_case
)
from app.ecommerce.order.use_cases.get_all_orders_use_case import (
    get_all_orders_use_case
)
from app.ecommerce.order.use_cases.get_order_by_id_use_case import (
    get_order_by_id_use_case
)
from app.ecommerce.order.use_cases.product_order_detail_use_case import (
    product_order_detail_use_case
)


blueprint = Blueprint("order", __name__, url_prefix="/orders")


@blueprint.route("/cart", methods=["GET"])
@token_required
def get_cart_order_detail():
    res = cart_order_detail_use_case()
    return Response(
        json.dumps(res.value),
        mimetype="application/json",
        status=STATUS_CODES[res.type]
    )


@blueprint.route("/product/<product_id>", methods=["GET"])
@token_required
def get_product_order_detail(product_id):
    req = validate_params_id(product_id)
    res = product_order_detail_use_case(req)
    return Response(
        json.dumps(res.value),
        mimetype="application/json",
        status=STATUS_CODES[res.type]
    )


@blueprint.route("/cart", methods=["POST"])
@token_required
def create_cart_order():
    data = request.get_json()
    req = validate_order_create_data(data)
    res = create_cart_order_use_case(req)
    return Response(
        json.dumps(res.value, cls=OrderSerializer),
        mimetype="application/json",
        status=STATUS_CODES[res.type]
    )


@blueprint.route("/product/<product_id>", methods=["POST"])
@token_required
def create_product_order(product_id):
    data = request.get_json()
    req = validate_order_create_data(data, product_id)
    res = create_product_order_use_case(req)
    return Response(
        json.dumps(res.value),
        mimetype="application/json",
        status=STATUS_CODES[res.type]
    )


@blueprint.route("/me", methods=["GET"])
@token_required
def get_user_orders():
    res = get_all_order_of_user_use_case()
    return Response(
        json.dumps(res.value, cls=OrderSerializer),
        mimetype="application/json",
        status=STATUS_CODES[res.type]
    )


@blueprint.route("/<order_id>", methods=["GET"])
@token_required
def get_order_by_id(order_id):
    req = validate_params_id(order_id)
    res = get_order_by_id_use_case(req)
    return Response(
        json.dumps(res.value, cls=OrderSerializer),
        mimetype="application/json",
        status=STATUS_CODES[res.type]
    )


@blueprint.route("/", methods=["GET"])
@admin_token_required
def get_all_orders():
    res = get_all_orders_use_case()
    return Response(
        json.dumps(res.value, cls=OrderSerializer),
        mimetype="application/json",
        status=STATUS_CODES[res.type]
    )


@blueprint.route("/<order_id>", methods=["DELETE"])
@admin_token_required
def delete_order(order_id):
    req = validate_params_id(order_id)
    res = delete_order_use_case(req)
    return Response(
        json.dumps(res.value),
        mimetype="application/json",
        status=STATUS_CODES[res.type]
    )


@blueprint.route("/cancle/<order_id>", methods=["PUT"])
@token_required
def cancle_order(order_id):
    req = validate_params_id(order_id)
    res = cancle_order_use_case(req)
    return Response(
        json.dumps(res.value),
        mimetype="application/json",
        status=STATUS_CODES[res.type]
    )
