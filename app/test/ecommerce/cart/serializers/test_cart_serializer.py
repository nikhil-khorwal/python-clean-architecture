import copy
import json
from unittest import TestCase

from flask import current_app
from app.ecommerce.cart.repository.cart_repository import CartRepository
from app.ecommerce.cart.serializers.cart_serializer import CartAdminSerializer, CartSerializer
from app.test.ecommerce.utils.sample_data.method import (
    create_address,
    create_admin_user,
    create_category,
    create_product,
)
from app.test.ecommerce.utils.sample_data.cart_data import (
    cart_request
)


class TestCartSerializer(TestCase):
    def setUp(self):
        self.payload = cart_request
        self.user = create_admin_user()
        self.address = create_address(self.user["email"])
        self.category = create_category()
        self.product = create_product(self.category["id"])

    def test_cart_serializer(self):
        with current_app.test_request_context("/?user_email={}".format(self.user["email"])):
            cart_repo = CartRepository()
            data = copy.deepcopy(cart_request)
            data.update({"product_id":self.product["id"]})
            cart_repo.add_product_to_cart(data)
            cart= cart_repo.get_user_cart().value

            
            expected_json = {
                    "id": cart.id,
                    "cart_items": [
                        {
                            "id": cart.cart_items[0].id,
                            "product": {
                                "id": cart.cart_items[0].product.id,
                                "title": cart.cart_items[0].product.title,
                                "desc": cart.cart_items[0].product.desc,
                                "images": [],
                                "price": cart.cart_items[0].product.price,
                                "stock": cart.cart_items[0].product.stock,
                                "gst_percentage": cart.cart_items[0].product.gst_percentage,
                                "discount_percentage": cart.cart_items[0].product.discount_percentage,
                                "category": {
                                    "id": cart.cart_items[0].product.category.id,
                                    "title": cart.cart_items[0].product.category.title
                                }
                            },
                            "quantity": cart.cart_items[0].quantity
                        }
                    ]
                }
            
            json_cart = json.dumps(cart, cls=CartSerializer)
            assert json.loads(json_cart) == expected_json
            