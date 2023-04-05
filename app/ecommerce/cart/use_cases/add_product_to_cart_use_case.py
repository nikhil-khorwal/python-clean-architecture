from app.core.error.response import ResponseTypes
from app.ecommerce.cart.repository.cart_repository import CartRepository
from app.core.error.response import (
    ResponseFailure,
    build_response_from_invalid_request
)

repository = CartRepository()


def add_product_to_cart_use_case(req):
    if not req:
        return build_response_from_invalid_request(req)
    try:
        return repository.add_product_to_cart(req.data)
    except Exception as err:
        return ResponseFailure(
            type_=ResponseTypes.SYSTEM_ERROR,
            message=err
        )
