from app.test.ecommerce.utils.sample_data.email_generator import (
    get_one_random_name,
    generate_random_number
)


address_request = {
    "house_no":get_one_random_name(),
    "street":get_one_random_name(),
    "landmark":get_one_random_name(),
    "pincode":564565,
    "city":get_one_random_name(),
    "state":get_one_random_name()
}

address_response = {
    "id": generate_random_number(),
    "house_no":get_one_random_name(),
    "street":get_one_random_name(),
    "landmark":get_one_random_name(),
    "pincode":564565,
    "city":get_one_random_name(),
    "state":get_one_random_name()
}