from app.ecommerce.cart.repository.cart_repository import CartRepository
from app.core.error.response import (
    ResponseFailure,
    build_response_from_invalid_request,
    ResponseTypes
)

repo = CartRepository()


def remove_product_from_cart_use_case(req):
    if not req:
        return build_response_from_invalid_request(req)
    try:
        return repo.remove_product_from_cart(req.data)
    except Exception as err:
        return ResponseFailure(
            type_=ResponseTypes.SYSTEM_ERROR,
            message=err
        )
