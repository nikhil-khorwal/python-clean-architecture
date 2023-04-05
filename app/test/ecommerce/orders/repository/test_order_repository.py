import copy
import json
from unittest import TestCase

from flask import current_app
import pytest
from app.core.error.response import ResponseTypes
from app.ecommerce.order.repository.order_repository import OrderRepository
from app.ecommerce.order.serializers.order_serializer import OrderSerializer
from app.test.ecommerce.utils.sample_data.method import (
    create_address,
    create_admin_user,
    create_cart,
    create_category,
    create_order,
    create_product,
)
from app.test.ecommerce.utils.sample_data.order_data import (
    order_request
)

class TestOrderRepository(TestCase):
    def setUp(self):
        self.payload = order_request
        self.repository = OrderRepository()
        self.user = create_admin_user()
        self.address = create_address(self.user["email"])
        self.category = create_category()
        self.product = create_product(self.category["id"])
        self.cart = create_cart(self.product["id"],self.user["email"])
        self.order = create_order(self.address["id"],self.user["email"])
    
    def test_cart_order_detail(self):
        with current_app.test_request_context("/?user_email={}".format(self.user["email"])):
            cart_detail = self.repository.cart_order_detail()
            self.assertEqual(cart_detail.value[0]["id"], self.cart["cart_items"][0]["id"])
            self.assertEqual(cart_detail.value[0]["product"], self.cart["cart_items"][0]["product"])
        
    def test_product_order_detail(self):
        with current_app.test_request_context("/?user_email={}".format(self.user["email"])):
            product_detail = self.repository.get_product_order_detail(self.product["id"])
            self.assertEqual(product_detail.value[0]["discount_percentage"], self.product["discount_percentage"])
            self.assertEqual(product_detail.value[0]["price"], self.product["price"])

    def test_create_cart_order(self):
        with current_app.test_request_context("/?user_email={}".format(self.user["email"])):
            data = self.payload
            data.update({"address_id":self.address["id"]})
            order = self.repository.create_cart_order(data)
            self.assertEqual(order.value["message"], "order create successfully")
            self.assertEqual(order.type, ResponseTypes.SUCCESS)
        
    def test_create_product_order(self):
        with current_app.test_request_context("/?user_email={}".format(self.user["email"])):
            data = self.payload
            data.update({"id":self.product["id"],"address_id":self.address["id"]})
            order = self.repository.create_product_order(data)
            self.assertEqual(order.value["message"], "order create successfully")
            self.assertEqual(order.type, ResponseTypes.SUCCESS)
    
    def test_delete_order(self):
        with current_app.test_request_context("/?user_email={}".format(self.user["email"])):
            delete_order = self.repository.delete_order(self.order["id"])
            self.assertEqual(delete_order.value["message"], "Order delete successfully")
            self.assertEqual(delete_order.type, ResponseTypes.SUCCESS)

    def test_cancle_order(self):
        with current_app.test_request_context("/?user_email={}".format(self.user["email"])):
            cancle_order = self.repository.cancle_order(self.order["id"])
            self.assertEqual(cancle_order.value["message"], "Order cancle successfully")
            self.assertEqual(cancle_order.type, ResponseTypes.SUCCESS)

    def test_get_all_users_order(self):
        with current_app.test_request_context("/?user_email={}".format(self.user["email"])):
            all_orders = self.repository.get_all_orders_users()
            self.assertGreater(len(all_orders.value),0)
            self.assertEqual(all_orders.type, ResponseTypes.SUCCESS)

    def test_get_all_order(self):
        with current_app.test_request_context("/?user_email={}".format(self.user["email"])):
            all_orders = self.repository.get_all_orders()
            self.assertGreater(len(all_orders.value),0)
            self.assertEqual(all_orders.type, ResponseTypes.SUCCESS)
        
    def test_get_order_by_id(self):
        with current_app.test_request_context("/?user_email={}".format(self.user["email"])):
            order = self.repository.get_order_by_id(self.order["id"])
            self.assertEqual(order.type, ResponseTypes.SUCCESS)
            self.assertEqual(self.order["id"],order.value.id)