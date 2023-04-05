from app.ecommerce.address.domain.address_domain import AddressDomain
from app.ecommerce.product.domain.product_domain import ProductDomain
from app.ecommerce.user.domain.user_domain import UserDomain
from dataclass_wizard import fromdict, asdict
import dataclasses

@dataclasses.dataclass
class OrderItemDomain:
    id: int
    product: ProductDomain
    quantity: int

    @classmethod
    def from_dict(cls, d):
        return fromdict(OrderItemDomain, d)

    def to_dict(self):
        return asdict(self)
    
    @staticmethod
    def from_db(result):
        return OrderItemDomain(
            id=result.id,
            product=ProductDomain.from_db(result.products),
            quantity=result.quantity)

@dataclasses.dataclass
class PaymentDomain:
    id:int
    price:float
    discount_price:float
    sub_total:float
    gst_price:float
    net_price:float
    @classmethod
    def from_dict(cls, d):
        return fromdict(PaymentDomain, d)

    def to_dict(self):
        return dataclasses.asdict(self)

    @staticmethod
    def from_db(result):
        return PaymentDomain(
            id=result.id,
            price=result.price,
            discount_price=result.discount_price,
            sub_total=result.sub_total,
            gst_price=result.gst_price,
            net_price=result.net_price)


@dataclasses.dataclass
class OrderDomain:
    id:int
    email:str
    phone:str
    user:UserDomain
    address:AddressDomain
    order_items: list[OrderItemDomain]
    payment:PaymentDomain

    @classmethod
    def from_dict(cls, d):
        return fromdict(OrderDomain, d)

    def to_dict(self):
        return dataclasses.asdict(self)
    
    @staticmethod
    def from_db(result):
        return OrderDomain(
            id=result.id,
            address=result.address,
            email=result.email,
            phone=result.phone,
            payment=PaymentDomain.from_db(result.payments),
            user=UserDomain.from_db(result.users),
            order_items=[OrderItemDomain.from_db(i) for i in result.order_items],
        )





