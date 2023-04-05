from app.ecommerce.category.repository.category_repository import (
    CategoryRepository
)
from app.core.error.response import (
    ResponseFailure,
    ResponseTypes,
    build_response_from_invalid_request
)

repository = CategoryRepository()


def category_get_by_id_use_case(request):
    if not request:
        return build_response_from_invalid_request(request)
    try:
        return repository.get_category_by_id(request.data)
    except Exception as exec:
        return ResponseFailure(
            type_=ResponseTypes.SYSTEM_ERROR,
            message=exec
        )
