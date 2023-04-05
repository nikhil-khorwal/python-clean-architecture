import dataclasses
from dataclass_wizard import fromdict

@dataclasses.dataclass
class AddressDomain:
    id:int
    house_no:str
    street:str
    landmark:str
    pincode:int
    city:str
    state:str

    @classmethod
    def from_dict(cls, d):
        return fromdict(AddressDomain, d)

    def to_dict(self):
        return dataclasses.asdict(self)

    @staticmethod
    def from_db(result):
        return AddressDomain(
            id=result.id,
            house_no=result.house_no,
            street=result.street,
            landmark=result.landmark,
            pincode=result.pincode,
            city=result.city,
            state=result.state
        )