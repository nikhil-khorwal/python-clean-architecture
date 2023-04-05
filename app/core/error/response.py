class ResponseTypes:
    BADREQUEST_ERROR = "BadRequest"
    RESOURCE_ERROR = "ResourceError"
    SYSTEM_ERROR = "SystemError"
    SUCCESS = "Success"
    UNAUTHORIZED = "Unauthorized"


STATUS_CODES = {
    ResponseTypes.SUCCESS: 200,
    ResponseTypes.RESOURCE_ERROR: 404,
    ResponseTypes.BADREQUEST_ERROR: 400,
    ResponseTypes.SYSTEM_ERROR: 500,
    ResponseTypes.UNAUTHORIZED: 401
}


class ResponseFailure:
    def __init__(self, type_, message, errors=[]):
        self.type = type_
        if isinstance(message, Exception):
            self.message = "{}".format(message)
            self.errors = {
                "code": message.__class__.__name__,
                "message": "{}".format(message)
            }
        else:
            self.message = message
            self.errors = errors

    @property
    def value(self):
        val = {
            "status": STATUS_CODES[self.type],
            "code": self.type,
            "message": self.message,
            "errors": self.errors
        }
        if len(self.errors) == 0:
            val.pop("errors")
        return val

    def __bool__(self):
        return False


class ResponseSuccess:
    def __init__(self, value=None):
        self.type = ResponseTypes.SUCCESS
        self.value = value

    def __bool__(self):
        return True


def build_response_from_invalid_request(invalid_request):
    errors = [
        {"code": err["parameter"], "meesage": err["message"]}
        for err in invalid_request.errors
    ]
    return ResponseFailure(
        type_=ResponseTypes.BADREQUEST_ERROR,
        message="Invalid request",
        errors=errors
    )