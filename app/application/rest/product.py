import json
from flask import Blueprint, Response, request
from app.core.methods.core_method import validate_params_id
from app.core.middleware.user_middleware import admin_token_required
from app.ecommerce.product.requests.product_request import (
    validate_crate_product_data,
    validate_product_data,
)
from app.core.error.response import STATUS_CODES
from app.ecommerce.product.use_cases.product_create_use_case import (
    product_create_use_case,
)
from app.ecommerce.product.use_cases.product_delete_use_case import (
    product_delete_use_case,
)
from app.ecommerce.product.use_cases.product_get_all_use_case import (
    product_get_all_use_case,
)
from app.ecommerce.product.use_cases.product_get_by_id_use_case import (
    product_get_by_id_use_case,
)
from app.ecommerce.product.use_cases.product_update_use_case import (
    product_update_use_case,
)
from app.ecommerce.product.serializers.product_serializer import (
    ProductSerializer)

blueprint = Blueprint("product", __name__, url_prefix="/products")


@blueprint.route("/", methods=["POST"])
@admin_token_required
def create_product():
    data = request.form.to_dict()

    req = validate_crate_product_data(data)
    res = product_create_use_case(req)
    return Response(
        json.dumps(res.value, cls=ProductSerializer),
        mimetype="application/json",
        status=STATUS_CODES[res.type],
    )


@blueprint.route("/", methods=["GET"])
def get_all_products():
    res = product_get_all_use_case()
    return Response(
        json.dumps(res.value, cls=ProductSerializer),
        mimetype="application/json",
        status=STATUS_CODES[res.type],
    )


@blueprint.route("/<product_id>", methods=["GET"])
def get_product_by_id(product_id):
    req = validate_params_id(product_id)
    res = product_get_by_id_use_case(req)
    return Response(
        json.dumps(res.value, cls=ProductSerializer),
        mimetype="application/json",
        status=STATUS_CODES[res.type],
    )


@blueprint.route("/<product_id>", methods=["PUT"])
@admin_token_required
def update_product(product_id):
    data = request.get_json()
    req = validate_product_data(data, id=product_id)
    res = product_update_use_case(req)
    return Response(
        json.dumps(res.value, cls=ProductSerializer),
        mimetype="application/json",
        status=STATUS_CODES[res.type],
    )


@blueprint.route("/<product_id>", methods=["DELETE"])
@admin_token_required
def delete_product(product_id):
    req = validate_params_id(product_id)
    res = product_delete_use_case(req)
    return Response(
        json.dumps(res.value, cls=ProductSerializer),
        mimetype="application/json",
        status=STATUS_CODES[res.type],
    )
