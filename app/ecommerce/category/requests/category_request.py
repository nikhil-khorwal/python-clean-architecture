from app.core.error.request import InvalidRequest, ValidRequest
from app.core.methods.core_method import check_required_field


def validate_create_category_data(data):
    req = check_required_field(["title"],data)
    if req.has_errors():
        return req
    return validate_category_data(data)


def validate_category_data(data, id=None):
    invalid_req = InvalidRequest()

    if (id is not None) and (not id.isnumeric()):
        invalid_req.add_error("params", "Is not integer")
    else:
        data["id"] = id

    if "title" in data and len(data["title"]) == 0:
        invalid_req.add_error("body", "Title not be empty")

    if invalid_req.has_errors():
        return invalid_req

    return ValidRequest(data=data)
