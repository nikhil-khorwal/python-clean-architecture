from unittest import TestCase

from flask import current_app
from app.core.error.response import ResponseTypes
from app.ecommerce.cart.repository.cart_repository import CartRepository

from app.test.ecommerce.utils.sample_data.method import (
    create_address,
    create_admin_user,
    create_cart,
    create_category,
    create_product,
    create_user,
)
from app.test.ecommerce.utils.sample_data.cart_data import cart_request


class TestCartRepository(TestCase):
    def setUp(self):
        self.payload = cart_request
        self.repository = CartRepository()
        self.user = create_admin_user()
        self.user2 = create_user()
        self.address = create_address(self.user["email"])
        self.category = create_category()
        self.product = create_product(self.category["id"])
        self.cart = create_cart(self.product["id"], self.user["email"])

    def test_cart_get_user_cart(self):
        with current_app.test_request_context(
            "/?user_email={}".format(self.user["email"])
        ):
            cart = self.repository.get_user_cart()
            self.assertEqual(self.cart["id"], cart.value.id)
            self.assertEqual(cart.type, ResponseTypes.SUCCESS)
    
    def test_cart_add_product_to_cart(self):
        with current_app.test_request_context(
            "/?user_email={}".format(self.user["email"])
        ):
            data = {
                "product_id":self.product["id"]
            }
            cart = self.repository.add_product_to_cart(data)
            self.assertEqual(cart.type, ResponseTypes.SUCCESS)
            self.assertEqual(cart.value["message"],"product added successfully")
    
    def test_cart_update_product_quantity(self):
        with current_app.test_request_context(
            "/?user_email={}".format(self.user["email"])
        ):
            data = {
                "id":self.cart["cart_items"][0]["id"],
                "quantity":self.cart["cart_items"][0]["quantity"]+1
            }
            cart = self.repository.update_quantity_of_cart(data)
            self.assertEqual(cart.type, ResponseTypes.SUCCESS)
            self.assertEqual(cart.value["message"],"update item successfully")

    def test_cart_remove_product_cart(self):
        with current_app.test_request_context(
            "/?user_email={}".format(self.user["email"])
        ):
            cart = self.repository.remove_product_from_cart(self.cart["cart_items"][0]["id"])
            self.assertEqual(cart.type, ResponseTypes.SUCCESS)
            self.assertEqual(cart.value["message"],"remove item successfully")

    def test_cart_get_all_cart(self):
        with current_app.test_request_context(
            "/?user_email={}".format(self.user["email"])
        ):
            cart = self.repository.get_all_carts()
            self.assertEqual(cart.type, ResponseTypes.SUCCESS)
            self.assertGreater(len(cart.value),0)
        
    def test_cart_get_cart_by_id(self):
        with current_app.test_request_context(
            "/?user_email={}".format(self.user["email"])
        ):
            cart = self.repository.get_cart_by_id(self.cart["id"])
            self.assertEqual(cart.type, ResponseTypes.SUCCESS)
            self.assertEqual(self.cart["id"], cart.value.id)