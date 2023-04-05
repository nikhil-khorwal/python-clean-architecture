from app.ecommerce.product.repository.product_repository import ProductRepository
from app.core.error.response import (
    ResponseFailure,
    ResponseTypes,
    build_response_from_invalid_request
)

repository = ProductRepository()


def product_delete_use_case(request):
    if not request:
        return build_response_from_invalid_request(request)
    try:
        return repository.delete_product(request.data)
    except Exception as exec:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, exec)
