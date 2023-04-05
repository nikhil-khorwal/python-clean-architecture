from app.ecommerce.product.repository.product_repository import ProductRepository
from app.core.error.response import (
    ResponseFailure,
    ResponseTypes,
    build_response_from_invalid_request
)

repository = ProductRepository()


def product_get_by_id_use_case(request):
    if not request:
        return build_response_from_invalid_request(request)
    try:
        return repository.get_product_by_id(request.data)
    except Exception as exec:
        return ResponseFailure(type_=ResponseTypes.SYSTEM_ERROR,message=exec,errors=[])

