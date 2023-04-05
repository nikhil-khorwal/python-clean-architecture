from app.core.error.response import (
        ResponseFailure,
        ResponseTypes,
        build_response_from_invalid_request
    )
from app.ecommerce.user.repository.user_repository import UserRepository


repository = UserRepository()


def user_get_by_id_use_case(request):
    if not request:
        return build_response_from_invalid_request(request)
    try:
        return repository.user_get_by_id(request.data)
    except Exception as exec:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, exec)
