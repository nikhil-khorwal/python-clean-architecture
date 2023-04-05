from app.core.error.response import build_response_from_invalid_request
from app.ecommerce.order.repository.order_repository import OrderRepository
from app.core.error.response import (
    ResponseFailure,
    ResponseTypes
)

repository = OrderRepository()


def create_product_order_use_case(request):
    if not request:
        return build_response_from_invalid_request(request)
    try:
        return repository.create_product_order(request.data)
    except Exception as err:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, err)
