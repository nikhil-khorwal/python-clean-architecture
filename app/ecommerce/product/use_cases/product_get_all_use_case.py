from app.ecommerce.product.repository.product_repository import ProductRepository
from app.core.error.response import (
    ResponseFailure,
    ResponseTypes
)

repository = ProductRepository()


def product_get_all_use_case():
    try:
        return repository.get_all_products()
    except Exception as err:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, err)
