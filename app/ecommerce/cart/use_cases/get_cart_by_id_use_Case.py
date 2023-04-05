from app.ecommerce.cart.repository.cart_repository import CartRepository
from app.core.error.response import (
    ResponseFailure,
    build_response_from_invalid_request,
    ResponseTypes
)

repo = CartRepository()


def get_cart_by_id_use_case(req):
    if not req:
        return build_response_from_invalid_request(req)
    try:
        return repo.get_cart_by_id(req.data)
    except Exception as err:
        return ResponseFailure(
            type_=ResponseTypes.SYSTEM_ERROR,
            message=err
        )
