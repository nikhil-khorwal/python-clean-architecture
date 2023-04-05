import sys,os
sys.path.append(os.getcwd()+"/ecommerce")
from app.core.error.request import InvalidRequest, ValidRequest
from app.core.methods.core_method import check_required_field

def validate_create_address_data(data):
    req = check_required_field(["house_no","street","landmark","pincode","city","state"],data)
    if req.has_errors():
        return req
    valid_data = validate_address_data(data)
    valid_data.data.pop("id")
    return valid_data

def validate_address_data(data, id=None):
    invalid_req = InvalidRequest()

    if (id is not None) and (not str(id).isnumeric()):
        invalid_req.add_error("params", "Is not integer")
    else:
        data["id"] = id
    if "house_no" in data and len(data["house_no"]) == 0:
        invalid_req.add_error("body", "house_no not be empty")
    if "street" in data and len(data["street"]) == 0:
        invalid_req.add_error("body", "street not be empty")
    if "landmark" in data and len(data["landmark"]) == 0:
        invalid_req.add_error("body", "landmark not be empty")
    if "pincode" in data:
        if not str(data["pincode"]).isnumeric() or len(str(data["pincode"])) != 6:
            invalid_req.add_error("body", "pincode is not valid")
    if "city" in data and len(data["city"]) == 0:
        invalid_req.add_error("body", "city not be empty")
    if "state" in data and len(data["state"]) == 0:
        invalid_req.add_error("body", "state not be empty")
    if invalid_req.has_errors():
        return invalid_req

    return ValidRequest(data=data)
