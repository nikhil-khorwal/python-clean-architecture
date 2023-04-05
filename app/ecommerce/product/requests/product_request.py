
from email.mime import image
from flask import request
from app.core.db.postgres_configuration import CategoryTable, PostgresConfiguration
from app.core.error.request import InvalidRequest, ValidRequest
from app.core.methods.core_method import check_required_field

def validate_crate_product_data(data):
    req = check_required_field(["title","desc","price","stock","category_id","discount_percentage","gst_percentage"],data)

    if 'images' not in request.files:
            req.add_error("required params","missing required param images")

    images = request.files.getlist("images")
    if len(images)==0 or images[0].filename == '':
        req.add_error("invalid params","atleast one image must")
    if req.has_errors():
        return req
    
    data.update({"images":images})
    return validate_product_data(data)

def validate_product_data(data, id=None):
    invalid_req = InvalidRequest()

    if (id is not None) and (not id.isnumeric()):
        invalid_req.add_error("params", "Is not integer")
    else:
        data["id"] = id
    if "title" in data and len(data["title"]) == 0:
        invalid_req.add_error("body", "Title not be empty")
    if "desc" in data and len(data["desc"]) == 0:
        invalid_req.add_error("body", "Discription not be empty")
    if "price" in data:
        if not str(data["price"]).isnumeric() or int(data["price"]) <= 0:
            invalid_req.add_error("body", "price is not valid")
    if "stock" in data:
        if not str(data["stock"]).isnumeric() or int(data["stock"]) < 0:
            invalid_req.add_error("body", "stock is not valid")
    if "category_id" in data:
        if (not str(data["category_id"]).isnumeric()) or (int(data["category_id"]) < 0):
            invalid_req.add_error("body", "category_id is not valid")
    if "discount_percentage" in data:
        if not str(data["discount_percentage"]).isnumeric() or int(data["discount_percentage"]) < 0:
            invalid_req.add_error("body", "discount_percentage is not valid")
    if "gst_percentage" in data:
        if not str(data["gst_percentage"]).isnumeric() or int(data["gst_percentage"]) < 0:
            invalid_req.add_error("body", "gst_percentage is not valid")
    if invalid_req.has_errors():
        return invalid_req

    return ValidRequest(data=data)
