from app.ecommerce.category.repository.category_repository import (
    CategoryRepository
)
from app.core.error.response import (
    ResponseFailure,
    ResponseTypes,
    build_response_from_invalid_request
)

repository = CategoryRepository()


def category_update_use_case(req):
    if not req:
        return build_response_from_invalid_request(invalid_request=req)
    try:
        return repository.update_category(req.data)
    except Exception as err:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, err)
