import re
from app.core.error.request import InvalidRequest, ValidRequest
from app.core.methods.core_method import  check_blank_field, check_required_field


EMAIL_REGEX = re.compile("[^@]+@[^@]+\.[^@]+") # noqa
PHONE_REGEX = re.compile("^(\+?\d{1,3}[\s-])?(?!0+\s+,?$)\d{10}\s*,?$") # noqa

def validate_user_signup_data(data):
    req = check_required_field(["first_name","last_name","email","password","phone"],data)
    if req.has_errors():
        return req

    invalid_req = InvalidRequest()

    if not EMAIL_REGEX.match(data["email"]):
        invalid_req.add_error("User data", "Email is not valid")
    if len(data["password"]) < 6:
        invalid_req.add_error("User data", "Password length is too short")
    if not PHONE_REGEX.match(data["phone"]):
        invalid_req.add_error("User data", "Phone number is not valid")
    
    if invalid_req.has_errors():
        return invalid_req
    else:
        return ValidRequest(data=data)


def validate_user_signin_data(data):
    req = check_required_field(["email","password"],data)
    if req.has_errors():
        return req

    invalid_req = InvalidRequest()

    if not EMAIL_REGEX.match(data["email"]):
        invalid_req.add_error("User data", "Email is not valid")
    if len(data["password"]) < 6:
        invalid_req.add_error("User data", "Password length is too short")
    
    if invalid_req.has_errors():
        return invalid_req
    else:
        return ValidRequest(data=data)
