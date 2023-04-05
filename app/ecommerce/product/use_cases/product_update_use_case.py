from app.ecommerce.product.repository.product_repository import ProductRepository
from app.core.error.response import (
    ResponseFailure,
    ResponseTypes,
    build_response_from_invalid_request
)

repository = ProductRepository()


def product_update_use_case(req):
    if not req:
        return build_response_from_invalid_request(invalid_request=req)
    try:
        return repository.update_product(req.data)
    except Exception as err:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, err)
