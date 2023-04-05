from app.ecommerce.order.repository.order_repository import OrderRepository
from app.core.error.response import (
    ResponseFailure,
    ResponseTypes,
    build_response_from_invalid_request
)

repository = OrderRepository()


def delete_order_use_case(request):
    if not request:
        return build_response_from_invalid_request(request)
    try:
        return repository.delete_order(request.data)
    except Exception as exec:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, exec)
