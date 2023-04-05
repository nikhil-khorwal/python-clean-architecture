from app.ecommerce.order.repository.order_repository import OrderRepository
from app.core.error.response import (
    ResponseFailure,
    ResponseTypes
)

repository = OrderRepository()


def cart_order_detail_use_case():
    try:
        return repository.cart_order_detail()
    except Exception as err:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, err)
