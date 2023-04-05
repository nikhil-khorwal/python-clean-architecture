from app.ecommerce.order.repository.order_repository import OrderRepository
from app.core.error.response import (
    ResponseFailure,
    ResponseTypes,
    build_response_from_invalid_request
)

repository = OrderRepository()


def create_cart_order_use_case(request):
    if not request:
        return build_response_from_invalid_request(request)
    try:
        return repository.create_cart_order(request.data)
    except Exception as err:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, err)
