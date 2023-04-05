from app.core.error.response import ResponseTypes
from app.ecommerce.cart.repository.cart_repository import CartRepository
from app.core.error.response import (
    ResponseFailure
)

repository = CartRepository()


def get_user_cart_use_case():
    try:
        return repository.get_user_cart()
    except Exception as err:
        return ResponseFailure(
            type_=ResponseTypes.SYSTEM_ERROR,
            message=err
        )
