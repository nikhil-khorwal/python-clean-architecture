import copy
import json
from unittest import TestCase

from flask import current_app
from app.ecommerce.order.repository.order_repository import OrderRepository
from app.ecommerce.order.serializers.order_serializer import OrderSerializer
from app.test.ecommerce.utils.sample_data.method import (
    create_address,
    create_admin_user,
    create_cart,
    create_category,
    create_product,
)
from app.test.ecommerce.utils.sample_data.order_data import (
    order_request
)


class TestOrderSerializer(TestCase):
    def setUp(self):
        self.payload = order_request
        self.user = create_admin_user()
        self.address = create_address(self.user["email"])
        self.category = create_category()
        self.product = create_product(self.category["id"])
        self.cart = create_cart(self.product["id"],self.user["email"])

    def test_order_serializer(self):
        with current_app.test_request_context("/?user_email={}".format(self.user["email"])):
            order_repo = OrderRepository()
            data = copy.deepcopy(self.payload)
            data.update({"address_id":self.address["id"]})
            order_res = order_repo.create_cart_order(data)
            order = order_res.value["data"]

            
            expected_json = {
                "id": order.id,
                "email":order.email,
                "phone":order.phone,
                "user":{
                    "id": order.user.id,
                    "first_name": order.user.first_name,
                    "last_name": order.user.last_name,
                    "email": order.user.email,
                    "phone": order.user.phone
                    },
                "address":{
                    "id":order.address.id,
                    "house_no":order.address.house_no,
                    "street":order.address.street,
                    "landmark":order.address.landmark,
                    "pincode":order.address.pincode,
                    "city":order.address.city,
                    "state":order.address.state
                },
                "order_items": [{
                    "id": i.id,
                    "product": {
                        "id": i.product.id,
                        "title": i.product.title,
                        "desc": i.product.desc,
                        "images": [{
                            "id":i.id,
                            "file_name":i.file_name,
                            "file_path":i.file_path
                        }
                        for i in i.product.images],
                        "price": i.product.price,
                        "gst_percentage": i.product.gst_percentage,
                        "discount_percentage": i.product.discount_percentage,
                        "stock": i.product.stock,
                        "category": {
                            "id": i.product.category.id,
                            "title": i.product.category.title,
                        }
                    },
                    "quantity": i.quantity
                }
                    for i in order.order_items
                ],
                "price_detail":{
                    "id":order.payment.id,
                    "price":order.payment.price,
                    "discount_price":order.payment.discount_price,
                    "sub_total":order.payment.sub_total,
                    "gst_price":order.payment.gst_price,
                    "net_price":order.payment.net_price
                    },
            }
            
            json_order = json.dumps(order, cls=OrderSerializer)
            assert json.loads(json_order) == expected_json
            