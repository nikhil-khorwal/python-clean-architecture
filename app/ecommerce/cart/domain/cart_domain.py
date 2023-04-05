from app.core.db.postgres_configuration import ImageTable, PostgresConfiguration
from app.ecommerce.product.domain.product_domain import ProductDomain
from app.ecommerce.user.domain.user_domain import UserDomain
from dataclass_wizard import fromdict, asdict
import dataclasses

@dataclasses.dataclass
class CartItemDomain:
    id: int
    product: ProductDomain
    quantity: int

    @classmethod
    def from_dict(cls, d):
        return fromdict(CartItemDomain, d)

    def to_dict(self):
        return dataclasses.asdict(self)
    
    @staticmethod
    def from_db(result):
        return CartItemDomain(
            id=result.id,
            product = ProductDomain.from_db(result.products),
            quantity=result.quantity
        )


@dataclasses.dataclass
class CartDomain:
    id: int
    user: UserDomain
    cart_items: list[CartItemDomain]

    @classmethod
    def from_dict(cls, d):
        return fromdict(CartDomain, d)

    def to_dict(self):
        return dataclasses.asdict(self)

    @staticmethod
    def from_db(result):
        return CartDomain(
            id=result.id,
            user=result.users,
            cart_items=[CartItemDomain.from_db(i) for i in result.cart_items]
        )
