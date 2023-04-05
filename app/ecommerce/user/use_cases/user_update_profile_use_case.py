from app.ecommerce.user.repository.user_repository import UserRepository
from app.core.error.response import ResponseFailure, ResponseTypes, build_response_from_invalid_request

repository = UserRepository()


def user_update_use_case(data):
    try:
        return repository.user_update_profile(data)
    except Exception as err:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, err)
