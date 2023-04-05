from app.ecommerce.category.repository.category_repository import (
    CategoryRepository
)
from app.core.error.response import (
    ResponseFailure,
    ResponseTypes,
    build_response_from_invalid_request
)

repository = CategoryRepository()


def category_delete_use_case(request):
    if not request:
        return build_response_from_invalid_request(request)
    try:
        return repository.delete_category(request.data)
    except Exception as exec:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, exec)
