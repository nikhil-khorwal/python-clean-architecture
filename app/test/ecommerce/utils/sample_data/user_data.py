from app.test.ecommerce.utils.sample_data.email_generator import (
    generate_random_emails,
    generate_random_number,
    get_one_random_name
)

admin_request = {
    "first_name": get_one_random_name(),
    "last_name": get_one_random_name(),
    "email": generate_random_emails(),
    "password": get_one_random_name(),
    "phone": "0123456789",
    "is_admin": True,
    "is_active": True,
    "is_delete": False
}

test_user_request = {
        "first_name": get_one_random_name(),
        "last_name": get_one_random_name(),
        "email": generate_random_emails(),
        "password": get_one_random_name(),
        "phone": "0123456789"
}

admin_response = {
    "id": generate_random_number(),
    "first_name": get_one_random_name(),
    "last_name": get_one_random_name(),
    "email": generate_random_emails(),
    "phone": "0123456789",
    "is_admin": True,
    "is_active": True,
    "is_delete": False
}
