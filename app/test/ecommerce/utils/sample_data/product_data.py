from app.test.ecommerce.utils.sample_data.email_generator import (
    generate_random_number,
    get_one_random_name
)

product_request = {
    "title": get_one_random_name(),
    "desc": get_one_random_name(),
    "price": generate_random_number(),
    "stock": generate_random_number(),
    "images": [],
    "category_id": generate_random_number(),
    "discount_percentage":5,
    "gst_percentage":18

}

product_response = {
    "id": generate_random_number(),
    "title": get_one_random_name(),
    "desc": get_one_random_name(),
    "stock": generate_random_number(),
    "price": generate_random_number(),
    "images": [],
    "category": {
        "id": generate_random_number(),
        "title": get_one_random_name()
    },
    "discount_percentage":5,
    "gst_percentage":18
}