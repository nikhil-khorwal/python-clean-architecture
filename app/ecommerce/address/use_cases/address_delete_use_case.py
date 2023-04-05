from app.ecommerce.address.repository.address_repository import (
    AddressRepository
)
from app.core.error.response import (
    ResponseFailure,
    ResponseTypes,
    build_response_from_invalid_request
)

repository = AddressRepository()


def address_delete_use_case(request):
    if not request:
        return build_response_from_invalid_request(request)
    try:
        return repository.delete_address(request.data)
    except Exception as exec:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, exec)
