from datetime import datetime
from app.test.ecommerce.utils.sample_data.email_generator import generate_random_emails
from app.test.ecommerce.utils.sample_data.email_generator import (
    generate_random_number,
    get_one_random_name
)
from app.test.ecommerce.utils.sample_data.product_data import product_response
from app.test.ecommerce.utils.sample_data.address_data import address_response

order_request = {
    "email": generate_random_emails(),
    "phone": "1234567981",
    "address": generate_random_number(),
}

order_item_response = {
    "id": generate_random_number(),
    "product": product_response,
    "quantity": generate_random_number(),
}

payment_response = {
    "id":generate_random_number(),
    "price":generate_random_number(),
    "discount_price":generate_random_number(),
    "sub_total":generate_random_number(),
    "gst_price":generate_random_number(),
    "net_price":generate_random_number()
}

order_response = {
    "id": generate_random_number(),
    "user": {
        "id": generate_random_number(),
        "first_name": get_one_random_name(),
        "last_name": get_one_random_name(),
        "password": get_one_random_name(),
        "email": generate_random_emails(),
        "phone": generate_random_number(),
        "is_active": True,
        "is_admin": True,
        "is_delete": False
    },
    "email": generate_random_emails(),
    "phone": generate_random_number(),
    "address": address_response,
    "order_items": [
        order_item_response,
        order_item_response,
        order_item_response
    ],
    "payment": payment_response
}
