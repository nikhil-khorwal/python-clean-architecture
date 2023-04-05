from app.test.ecommerce.utils.sample_data.email_generator import (
    get_one_random_name,
    generate_random_number
)


category_request = {
    "title": get_one_random_name(),
}

category_response = {
    "id": generate_random_number(),
    "title": get_one_random_name()
}
