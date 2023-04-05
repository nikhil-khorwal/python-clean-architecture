from datetime import datetime
from math import floor
from app.core.error.request import InvalidRequest, ValidRequest

from werkzeug.utils import secure_filename

def calculate_cart_product_price(list_of_products):
        price=0
        sub_total=0
        discount_price=0
        gst_price=0
        net_price=0

        res = {}
        for i in list_of_products:
            price = (i.quantity * i.products.price)
            discount_price = floor((price * i.products.discount_percentage)/100)
            sub_total = floor(price - discount_price)
            gst_price = floor((sub_total * i.products.gst_percentage)/100)
            net_price = floor(gst_price+sub_total)
            response = {
                "price":price,
                "discount_price":discount_price,
                "sub_total":sub_total,
                "gst_price":gst_price,
                "net_price":net_price
            }
            res.update({f"product_{i.products.id}":response})
        return res

def calculate_product_price(product):
    price=0
    sub_total=0
    discount_price=0
    gst_price=0
    net_price=0

    price = product.price
    discount_price = floor((price*product.discount_percentage)/100)
    sub_total = floor(price - discount_price)
    gst_price = floor((sub_total*product.gst_percentage)/100)
    net_price = floor(gst_price+sub_total)
    response = {
        "price":price,
        "discount_price":discount_price,
        "sub_total":sub_total,
        "gst_price":gst_price,
        "net_price":net_price
    }
    return response

def check_required_field(params, data)->InvalidRequest:
    invalid_req = InvalidRequest()
    for i in params:
        if i not in data:
            invalid_req.add_error(f"required params","missing required param "+i)
    if invalid_req.has_errors():
        return invalid_req
    else:
        return check_blank_field(params,data,invalid_req)

def check_blank_field(params, data, invalid_req)->InvalidRequest:
    for i in params:
        if type(data[i])==int or type(data[i])==float:
            if data[i]<1:
                invalid_req.add_error(f"invalid params",i + " should greater then 0")
        else:
            if len(data[i]) == 0:
                invalid_req.add_error(f"invalid params",i + " could not be blank")
    return invalid_req

def validate_params_id(data):
    invalid_req = InvalidRequest()
    if not str(data).isnumeric():
        invalid_req.add_error("params", "Is not integer")
        return invalid_req
    return ValidRequest(data=data)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_extension(filename):
    return filename.rsplit('.', 1)[1].lower()

def create_file_name(filename):
    time = datetime.now()
    new_filename = secure_filename(f"{time.date()}{time.time()}").replace('-',"").replace(".","")
    return f"{new_filename}.{get_file_extension(filename)}"