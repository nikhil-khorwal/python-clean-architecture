from app.core.error.response import ResponseTypes
from app.ecommerce.cart.repository.cart_repository import CartRepository
from app.core.error.response import (
    ResponseFailure
)

repository = CartRepository()


def get_all_carts_use_case():
    try:
        return repository.get_all_carts()
    except Exception as err:
        return ResponseFailure(
            type_=ResponseTypes.SYSTEM_ERROR,
            message=err
        )
