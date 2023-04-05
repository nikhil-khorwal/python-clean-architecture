import dataclasses
from dataclass_wizard import fromdict

@dataclasses.dataclass
class UserDomain:
    id: int
    first_name: str
    last_name: str
    email: str
    phone: str
    is_active: bool
    is_admin: bool
    is_delete: bool

    @classmethod
    def from_dict(cls, d):
        return fromdict(UserDomain, d)

    def to_dict(self):
        to_dict = dataclasses.asdict(self)
        return to_dict

    @staticmethod
    def from_db(result):
        return UserDomain(
            id=result.id,
            first_name=result.first_name,
            last_name=result.last_name,
            email=result.email,
            phone=result.phone,
            is_active=result.is_active,
            is_admin=result.is_admin,
            is_delete=result.is_delete
        )