from app.ecommerce.user.repository.user_repository import UserRepository
from app.core.error.response import ResponseFailure, ResponseTypes


repository = UserRepository()


def user_get_all_users_use_case():
    try:
        return repository.user_get_all_users()
    except Exception as err:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, err)
