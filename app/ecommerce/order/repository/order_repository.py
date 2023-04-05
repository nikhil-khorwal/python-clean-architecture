from datetime import datetime
from operator import and_
from app.core.methods.core_method import (
    calculate_cart_product_price,
    calculate_product_price,
)
from flask import request
from app.ecommerce.cart.domain.cart_domain import CartItemDomain
from app.core.error.response import ResponseFailure, ResponseSuccess, ResponseTypes
from app.core.db.postgres_configuration import (
    AddressTable,
    CartItemTable,
    CartTable,
    ImageTable,
    OrderEnum,
    OrderItemTable,
    OrderTable,
    PaymentTable,
    PostgresConfiguration,
    ProductTable,
    UserTable,
)
from sqlalchemy import and_, or_
from app.ecommerce.order.domain.order_domain import (
    OrderDomain
)
from app.ecommerce.product.domain.product_domain import ProductDomain


class OrderRepository:
    def __init__(self):
        self.session = PostgresConfiguration.get_session()

    def cart_order_detail(self):
        user_email = request.args["user_email"]
        result = (
            self.session.query(CartItemTable)
            .join(CartTable)
            .join(UserTable)
            .filter(UserTable.email == user_email)
            .all()
        )
        res_price = calculate_cart_product_price(result)
        res = []
        for i, j in zip(result, res_price.values()):
            cart_item = CartItemDomain.from_db(i).to_dict()
            cart_item.update({"price_detail": j})
            res.append(cart_item)

        return ResponseSuccess(res)

    def get_product_order_detail(self, id):
        result = self.session.query(ProductTable).filter(ProductTable.id == id).first()
        if result is None:
            return ResponseFailure(
                type_=ResponseTypes.BADREQUEST_ERROR,
                message="No product found for this id!"
            )
        res_price = calculate_product_price(result)
        res = []
        cart_item = ProductDomain.from_db(result).to_dict()
        images = (
            self.session.query(ImageTable)
            .filter(ImageTable.product_id == cart_item["id"])
            .all()
        )
        cart_item.update(
            {"images": [i.file_path for i in images], "price_detail": res_price}
        )
        res.append(cart_item)
        return ResponseSuccess(res)

    def create_cart_order(self, data):

        address = (
            self.session.query(AddressTable).filter_by(id=data["address_id"]).first()
        )
        if address is None:
            return ResponseFailure(
                type_=ResponseTypes.BADREQUEST_ERROR,
                message="No address found for this id!"
            )

        user_email = request.args["user_email"]
        exist_user = self.session.query(UserTable).filter_by(email=user_email).first()
        result = (
            self.session.query(CartItemTable)
            .join(CartTable)
            .join(UserTable)
            .filter(UserTable.email == user_email)
            .all()
        )

        if len(result) < 1:
            return ResponseFailure(
                type_=ResponseTypes.BADREQUEST_ERROR,
                message="cart is empty!"
            )

        res = calculate_cart_product_price(result)
        price = 0
        discount_price = 0
        sub_total = 0
        gst_price = 0
        net_price = 0
        for i in res.values():
            price += i["price"]
            discount_price += i["discount_price"]
            sub_total += i["sub_total"]
            gst_price += i["gst_price"]
            net_price += i["net_price"]

        new_payment = PaymentTable(
            price=price,
            discount_price=discount_price,
            sub_total=sub_total,
            gst_price=gst_price,
            net_price=net_price,
        )
        self.session.add(new_payment)
        self.session.commit()

        new_order = OrderTable(
            email=data["email"],
            phone=data["phone"],
            address_id=data["address_id"],
            status=OrderEnum.PENDING,
            user_id=exist_user.id,
            payment_id=new_payment.id,
        )
        self.session.add(new_order)
        self.session.commit()
        order_items = []
        for i in result:
            order_item = OrderItemTable(
                quantity=i.quantity, product_id=i.products.id, order_id=new_order.id
            )
            order_items.append(order_item)
            self.session.add(order_item)
            self.session.commit()
        response = self.get_order_by_id(new_order.id).value
        return ResponseSuccess(
            {"message": "order create successfully", "data": response}
        )

    def create_product_order(self, data):
        user_email = request.args["user_email"]
        exist_user = self.session.query(UserTable).filter_by(email=user_email).first()
        result = (
            self.session.query(ProductTable)
            .filter(ProductTable.id == data["id"])
            .first()
        )
        if result is None:
            return ResponseFailure(
                type_=ResponseTypes.BADREQUEST_ERROR,
                message="No product found for this id!"
            )

        res = calculate_product_price(result)
        new_payment = PaymentTable(
            price=res["price"],
            discount_price=res["discount_price"],
            sub_total=res["sub_total"],
            gst_price=res["gst_price"],
            net_price=res["net_price"],
        )
        self.session.add(new_payment)
        self.session.commit()

        new_order = OrderTable(
            email=data["email"],
            phone=data["phone"],
            address_id=data["address_id"],
            user_id=exist_user.id,
            payment_id=new_payment.id,
        )
        self.session.add(new_order)
        self.session.commit()

        new_order_item = OrderItemTable(
            quantity=1, product_id=result.id, order_id=new_order.id
        )
        self.session.add(new_order_item)
        self.session.commit()

        response = self.get_order_by_id(new_order.id).value
        return ResponseSuccess(
            {"message": "order create successfully", "data": response}
        )

    def delete_order(self, id):
        order = self.session.query(OrderTable).filter(OrderTable.id == id).first()
        if order is None:
            return ResponseFailure(
                type_=ResponseTypes.BADREQUEST_ERROR,
                message="No order found for this id!"
            )
        order.is_delete = True
        payments = self.session.query(PaymentTable)\
                           .filter(id == order.payment_id).first()
        payments.is_delete = True
        orderItems = self.session.query(OrderItemTable)\
                           .filter(OrderItemTable.order_id == order.id).all()
        for i in orderItems:
            i.is_delete = True
        self.session.commit()
        return ResponseSuccess({"message": "Order delete successfully"})

    def cancle_order(self, id):
        user_email = request.args["user_email"]
        order = (
            self.session.query(OrderTable)
            .join(UserTable)
            .filter(and_(OrderTable.id == id, UserTable.email == user_email))
            .first()
        )
        if order is None:
            return ResponseFailure(
                type_=ResponseTypes.BADREQUEST_ERROR,
                message="No order found for this id!"
            )
        order.status = OrderEnum.CANCELLED
        order.updated_at = datetime.now()
        self.session.commit()
        return ResponseSuccess({"message": "Order cancle successfully"})

    def get_all_orders_users(self):
        user_email = request.args["user_email"]

        orders = (
            self.session.query(OrderTable)
            .join(UserTable)
            .filter(UserTable.email == user_email)
            .all()
        )
        response = []
        for i in orders:
            response.append(OrderDomain.from_db(i))
        return ResponseSuccess(response)

    def get_all_orders(self):
        orders = self.session.query(OrderTable).all()
        response = []
        for i in orders:
            response.append(OrderDomain.from_db(i))
        return ResponseSuccess(response)

    def get_order_by_id(self, id):
        user_email = request.args["user_email"]
        exist_user = (
            self.session.query(UserTable).filter(UserTable.email == user_email).first()
        )
        order = (
            self.session.query(OrderTable)
            .join(UserTable)
            .filter(
                and_(
                    OrderTable.id == id,
                    or_(UserTable.email == user_email, exist_user.is_admin == True),
                )
            )
            .first()
        )
        if order is None:
            return ResponseFailure(
                type_=ResponseTypes.BADREQUEST_ERROR,
                message="No order found for this id!"
            )

        return ResponseSuccess(OrderDomain.from_db(order))
