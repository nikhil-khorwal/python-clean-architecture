import dataclasses
from typing import List
from app.ecommerce.category.domain.category_domain import CategoryDomain
from dataclass_wizard import fromdict, asdict


@dataclasses.dataclass
class ImageDomain:
    id:int
    file_name:str
    file_path:str


    @classmethod
    def from_dict(cls, d):
        return fromdict(ImageDomain, d)

    def to_dict(self):
        return dataclasses.asdict(self)

    @staticmethod
    def from_db(result):
        return ImageDomain(
            id = result.id,
            file_name = result.file_name,
            file_path = result.file_path
        )

@dataclasses.dataclass
class ProductDomain:
    id: int
    title: str
    desc: str
    price: int
    stock: int
    discount_percentage: float
    gst_percentage: float
    category: CategoryDomain
    images: list


    @classmethod
    def from_dict(cls, d):
        return fromdict(ProductDomain, d)

    def to_dict(self):
        return dataclasses.asdict(self)

    @staticmethod
    def from_db(result):
        return ProductDomain(
            id=result.id,
            title=result.title,
            desc=result.desc,
            price=result.price,
            stock=result.stock,
            discount_percentage= result.discount_percentage,
            gst_percentage= result.gst_percentage,
            category=CategoryDomain.from_db(result.categories),
            images=[ImageDomain.from_db(i) for i in result.images]
        )


