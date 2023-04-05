import sys,os
sys.path.append(os.getcwd()+"/ecommerce")
from app.core.error.request import InvalidRequest, ValidRequest
from app.core.methods.core_method import check_required_field

def validate_cart_create_data(data):
    req = check_required_field(["product_id"],data)
    
    if (str(data["product_id"]) is not None) and (not str(data["product_id"]).isnumeric()):
        req.add_error("params", "Is not integer")

    if req.has_errors():
        return req

    return ValidRequest(data=data)

def validate_cart_update_data(data, id=None):
    invalid_req = InvalidRequest()

    if (str(id) is not None) and (not str(id).isnumeric()):
        invalid_req.add_error("params", "Is not integer")
    else:
        data["id"] = id
    if "quantity" in data:
        if not str(data["quantity"]).isnumeric() or int(data["quantity"]) < 0:
            invalid_req.add_error("body", "quantity is not valid")

    if invalid_req.has_errors():
        return invalid_req

    return ValidRequest(data=data)
