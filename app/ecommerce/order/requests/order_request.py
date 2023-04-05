from flask import request
from app.core.db.postgres_configuration import AddressTable, CartItemTable, CartTable, CategoryTable, PostgresConfiguration, UserTable
from app.core.error.request import InvalidRequest, ValidRequest

session = PostgresConfiguration.get_session()

def validate_order_create_data(data):
    invalid_req = InvalidRequest()
        
    if "email" in data and len(data["email"]) == 0:
        invalid_req.add_error("body", "email not be empty")
    if "phone" in data and len(data["phone"]) == 0:
        invalid_req.add_error("body", "phone not be empty")
    if "address_id" in data:
        if (not str(data["address_id"]).isnumeric()) or (int(data["address_id"]) < 0):
            invalid_req.add_error("body", "address_id is not valid")
            
    if invalid_req.has_errors():
        return invalid_req

    return ValidRequest(data=data)


