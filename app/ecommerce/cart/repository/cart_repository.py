from flask import request
from sqlalchemy import and_, select
from app.core.error.response import ResponseFailure, ResponseTypes
from app.core.db.postgres_configuration import CategoryTable, ImageTable
from app.ecommerce.category.domain.category_domain import CategoryDomain
from app.ecommerce.product.repository.product_repository import ProductRepository
from app.ecommerce.user.repository.user_repository import UserRepository
from app.ecommerce.product.domain.product_domain import ProductDomain
from app.ecommerce.cart.domain.cart_domain import CartItemDomain
from app.ecommerce.user.domain.user_domain import UserDomain
from app.core.db.postgres_configuration import CartItemTable, ProductTable
from app.core.error.response import ResponseSuccess
from app.ecommerce.cart.domain.cart_domain import CartDomain
from app.core.db.postgres_configuration import CartTable, UserTable
from app.core.db.postgres_configuration import PostgresConfiguration


class CartRepository:
    def __init__(self):
        self.session = PostgresConfiguration.get_session()
        self.user_repo = UserRepository()
        self.pro_repo = ProductRepository()

    def get_user_cart(self):
        user_email = request.args["user_email"]
        result = (
            self.session.query(CartTable)
            .join(UserTable)
            .filter(UserTable.email == user_email)
            .first()
        )
        if result is None:
            return ResponseFailure(
                type_=ResponseTypes.SUCCESS,
                message="Cart is empty!"
            )
        res = CartDomain.from_db(result)
        return ResponseSuccess(res)

    def add_product_to_cart(self, data):
        product = (
            self.session.query(ProductTable).filter_by(id=data["product_id"]).first()
        )
        if product is None:
            return ResponseFailure(
                type_=ResponseTypes.BADREQUEST_ERROR,
                message="No product found for this id!"
            )

        user_email = request.args["user_email"]
        user = self.session.query(UserTable).filter_by(email=user_email).first()
        cart = (
            self.session.query(CartTable).filter(CartTable.user_id == user.id).first()
        )
        if cart is None:
            cart = CartTable(user_id=user.id)
            self.session.add(cart)
        cart_item = (
            self.session.query(CartItemTable)
            .filter(
                and_(
                    CartItemTable.product_id == data["product_id"],
                    CartItemTable.cart_id == cart.id,
                )
            )
            .first()
        )
        if cart_item is None:
            cart_item = CartItemTable(
                quantity=1, cart_id=cart.id, product_id=data["product_id"]
            )
            self.session.add(cart_item)
        else:
            cart_item.quantity += 1
        self.session.commit()
        return ResponseSuccess(value={"message": "product added successfully"})

    def update_quantity_of_cart(self, data):
        user_email = request.args["user_email"]
        user = self.session.query(UserTable).filter_by(email=user_email).first()
        result = (
            self.session.query(CartItemTable)
            .join(CartTable)
            .filter(CartTable.user_id == user.id)
            .filter(CartItemTable.id == data["id"])
            .first()
        )

        if result is None:
            return ResponseFailure(
                type_=ResponseTypes.BADREQUEST_ERROR,
                message="No item found for this id!"
            )

        if data["quantity"] <= 0:
            self.session.delete(result)
        else:
            result.quantity = data["quantity"]
        self.session.commit()
        return ResponseSuccess(value={"message": "update item successfully"})

    def remove_product_from_cart(self, id):
        result = (
            self.session.query(CartItemTable).filter(CartItemTable.id == id).first()
        )
        if result is None:
            return ResponseFailure(
                type_=ResponseTypes.BADREQUEST_ERROR,
                message="No item found for this id!"
            )
        self.session.delete(result)
        self.session.commit()
        return ResponseSuccess(value={"message": "remove item successfully"})

    def get_all_carts(self):
        result = self.session.query(CartTable).all()
        res = []
        for i in result:
            res.append(CartDomain.from_db(i))
        return ResponseSuccess(res)

    def get_cart_by_id(self, id):
        result = self.session.query(CartTable).filter(CartTable.id == id).first()
        if result is None:
            return ResponseFailure(
                type_=ResponseTypes.BADREQUEST_ERROR,
                message="Cart is empty!"
            )
        res = CartDomain.from_db(result)
        return ResponseSuccess(res)
