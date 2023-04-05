from app.ecommerce.order.repository.order_repository import OrderRepository
from app.core.error.response import (
    ResponseFailure,
    ResponseTypes
)

repository = OrderRepository()


def get_all_orders_use_case():
    try:
        return repository.get_all_orders()
    except Exception as err:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, err)
