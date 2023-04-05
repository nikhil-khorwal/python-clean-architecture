from unittest import TestCase

from app.ecommerce.order.domain.order_domain import OrderDomain, OrderItemDomain, PaymentDomain
from app.test.ecommerce.utils.sample_data.method import (
    create_address,
    create_admin_user,
    create_cart,
    create_category,
    create_product,
)
from app.test.ecommerce.utils.sample_data.order_data import (
    order_response,
    order_item_response,
    payment_response
)


class TestOrderDomain(TestCase):
    def setUp(self):
        self.payload = order_response
        self.user = create_admin_user()
        self.address = create_address(self.user["email"])
        self.category = create_category()
        self.product = create_product(self.category["id"])
        self.cart = create_cart(self.product["id"],self.user["email"])

    def test_order_domain(self):
        order_domain = OrderDomain(**self.payload)
        self.assertEqual(order_domain.user["email"], self.payload["user"]["email"])

    def test_order_from_dict(self):
        order_domain = OrderDomain.from_dict(self.payload)      
        self.assertEqual(order_domain.user.email, self.payload["user"]["email"])

    def test_order_to_dict(self):
        order_domain = OrderDomain.from_dict(self.payload)
        order_dict = order_domain.to_dict()
        self.assertEqual(order_dict["user"]["email"], self.payload["user"]["email"])


class TestOrderItemDomain(TestCase):
    def setUp(self):
        self.payload = order_item_response
        self.user = create_admin_user()
        self.address = create_address(self.user["email"])
        self.category = create_category()
        self.product = create_product(self.category["id"])
        self.cart = create_cart(self.product["id"],self.user["email"])

    def test_order_item_domain(self):
        order_item_domain = OrderItemDomain(**self.payload)
        self.assertEqual(order_item_domain.quantity, self.payload["quantity"])

    def test_order_item_from_dict(self):
        order_item_domain = OrderItemDomain.from_dict(self.payload)
        self.assertEqual(order_item_domain.quantity, self.payload["quantity"])

    def test_order_item_to_dict(self):
        order_item_domain = OrderItemDomain.from_dict(self.payload)
        order_item_dict = order_item_domain.to_dict()
        self.assertEqual(order_item_dict["quantity"], self.payload["quantity"])

class TestPaymentDomain(TestCase):
    def setUp(self):
        self.payload = payment_response
        self.user = create_admin_user()
        self.address = create_address(self.user["email"])
        self.category = create_category()
        self.product = create_product(self.category["id"])
        self.cart = create_cart(self.product["id"],self.user["email"])

    def test_payment_domain(self):
        payment_domain = PaymentDomain(**self.payload)
        self.assertEqual(payment_domain.discount_price, self.payload["discount_price"])

    def test_payment_from_dict(self):
        payment_domain = PaymentDomain.from_dict(self.payload)
        self.assertEqual(payment_domain.discount_price, self.payload["discount_price"])

    def test_payment_to_dict(self):
        payment_domain = PaymentDomain.from_dict(self.payload)
        payment_dict = payment_domain.to_dict()
        self.assertEqual(payment_dict["discount_price"], self.payload["discount_price"])
