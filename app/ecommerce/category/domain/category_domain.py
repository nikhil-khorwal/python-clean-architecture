import dataclasses
from dataclass_wizard import fromdict

@dataclasses.dataclass
class CategoryDomain:
    id: int
    title: str

    @classmethod
    def from_dict(cls, d):
        return fromdict(CategoryDomain, d)

    def to_dict(self):
        return dataclasses.asdict(self)

    @staticmethod
    def from_db(result):
        return CategoryDomain(
            id=result.id,
            title=result.title
        )