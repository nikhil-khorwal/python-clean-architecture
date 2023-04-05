from datetime import datetime
from app.test.ecommerce.utils.sample_data.email_generator import generate_random_emails
from app.test.ecommerce.utils.sample_data.email_generator import (
    generate_random_number,
    get_one_random_name
)
from app.test.ecommerce.utils.sample_data.product_data import product_response

cart_request = {
    "product_id": generate_random_number(),
}

cart_item_response = {
    "id": generate_random_number(),
    "product": product_response,
    "quantity": generate_random_number(),
}


cart_response = {
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
    "cart_items": [
        cart_item_response,
        cart_item_response,
        cart_item_response
    ]
}
