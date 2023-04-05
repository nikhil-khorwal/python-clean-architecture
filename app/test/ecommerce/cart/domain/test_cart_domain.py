from unittest import TestCase

import pytest
from app.ecommerce.cart.domain.cart_domain import CartDomain, CartItemDomain
from app.test.ecommerce.utils.sample_data.method import (
    create_address,
    create_admin_user,
    create_category,
    create_product,
)
from app.test.ecommerce.utils.sample_data.cart_data import (
    cart_response,
    cart_item_response
)


class TestCartDomain(TestCase):
    def setUp(self):
        self.payload = cart_response
        self.user = create_admin_user()
        self.address = create_address(self.user["email"])
        self.category = create_category()
        self.product = create_product(self.category["id"])

    def test_cart_domain(self):
        cart_domain = CartDomain(**self.payload)
        self.assertEqual(cart_domain.user["email"], self.payload["user"]["email"])

    def test_cart_from_dict(self):
        cart_domain = CartDomain.from_dict(self.payload)      
        self.assertEqual(cart_domain.user.email, self.payload["user"]["email"])

    def test_cart_to_dict(self):
        cart_domain = CartDomain.from_dict(self.payload)
        cart_dict = cart_domain.to_dict()
        self.assertEqual(cart_dict["user"]["email"], self.payload["user"]["email"])


class TestCartItemDomain(TestCase):
    def setUp(self):
        self.payload = cart_item_response
        self.user = create_admin_user()
        self.address = create_address(self.user["email"])
        self.category = create_category()
        self.product = create_product(self.category["id"])

    def test_cart_item_domain(self):
        cart_item_domain = CartItemDomain(**self.payload)
        self.assertEqual(cart_item_domain.quantity, self.payload["quantity"])

    def test_cart_item_from_dict(self):
        cart_item_domain = CartItemDomain.from_dict(self.payload)
        self.assertEqual(cart_item_domain.quantity, self.payload["quantity"])

    def test_cart_item_to_dict(self):
        cart_item_domain = CartItemDomain.from_dict(self.payload)
        cart_item_dict = cart_item_domain.to_dict()
        self.assertEqual(cart_item_dict["quantity"], self.payload["quantity"])
