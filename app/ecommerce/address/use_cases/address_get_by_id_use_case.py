from app.ecommerce.address.repository.address_repository import (
    AddressRepository
)
from app.core.error.response import (
    ResponseFailure,
    ResponseTypes,
    build_response_from_invalid_request
)

repository = AddressRepository()


def address_get_by_id_use_case(request):
    if not request:
        return build_response_from_invalid_request(request)
    try:
        return repository.get_address_by_id(request.data)
    except Exception as exec:
        return ResponseFailure(
            type_=ResponseTypes.SYSTEM_ERROR,
            message=exec
        )
