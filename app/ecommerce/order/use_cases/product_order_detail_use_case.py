from app.core.error.response import build_response_from_invalid_request
from app.ecommerce.order.repository.order_repository import OrderRepository
from app.core.error.response import (
    ResponseFailure,
    ResponseTypes
)

repository = OrderRepository()


def product_order_detail_use_case(request):
    if not request:
        return build_response_from_invalid_request(request)
    try:
        return repository.get_product_order_detail(request.data)
    except Exception as err:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, err)
