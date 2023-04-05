from app.ecommerce.address.repository.address_repository import (
    AddressRepository
)
from app.core.error.response import (
    ResponseFailure,
    ResponseTypes,
    build_response_from_invalid_request
)

repository = AddressRepository()


def address_update_use_case(req):
    if not req:
        return build_response_from_invalid_request(invalid_request=req)
    try:
        return repository.update_address(req.data)
    except Exception as err:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, err)
