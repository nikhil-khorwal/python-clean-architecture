from app.ecommerce.address.repository.address_repository import (
    AddressRepository
)
from app.core.error.response import (
    ResponseFailure,
    ResponseTypes
)

repository = AddressRepository()


def address_get_all_for_user_use_case():
    try:
        return repository.get_all_user_addresses()
    except Exception as err:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, err)
