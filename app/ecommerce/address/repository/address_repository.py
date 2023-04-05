import json
from flask import request
from sqlalchemy import and_, or_
from app.core.error.response import ResponseFailure, ResponseTypes
from app.core.error.response import ResponseSuccess
from app.core.db.postgres_configuration import PostgresConfiguration, AddressTable, UserTable
from app.ecommerce.address.domain.address_domain import AddressDomain
from app.ecommerce.user.domain.user_domain import UserDomain


class AddressRepository:
    def __init__(self):
        self.session = PostgresConfiguration.get_session()

    def create_address(self, data):
        user_email = request.args["user_email"]
        exist_user = self.session.query(UserTable).filter(UserTable.email==user_email).first()
        new_address = AddressTable(**data)
    
        new_address.user_id = exist_user.id
        self.session.add(new_address)
        self.session.commit()
        return ResponseSuccess({
            "message": "Data added successfully",
            "data": AddressDomain.from_db(new_address)
        })

    def get_all_addresses(self):
        all_addresses = self.session.query(AddressTable).all()
        all_addresses_obj = [
            AddressDomain.from_db(i)
            for i in all_addresses
        ]
        return ResponseSuccess(
            all_addresses_obj
        )

    def get_all_user_addresses(self):
        user_email = request.args["user_email"]
        all_addresses = self.session.query(AddressTable)\
                            .join(UserTable)\
                            .filter(UserTable.email == user_email).all()

        all_addresses_obj = [
            AddressDomain.from_db(i)
            for i in all_addresses
        ]
        return ResponseSuccess(
            all_addresses_obj
        )

    def get_address_by_id(self, id):
        user_email = request.args["user_email"]
        exist_user = self.session.query(UserTable).filter(UserTable.email==user_email).first()
        address = self.session.query(AddressTable)\
                    .join(UserTable)\
                            .filter(and_(
                                    AddressTable.id == id,
                                    or_(
                                        UserTable.email == user_email,
                                        exist_user.is_admin==True
                                    )
                                )
                            ).first()
        if(address is None):
            return ResponseFailure(
                type_=ResponseTypes.BADREQUEST_ERROR,
                message="No address found for this id!"
            )
        address_obj = AddressDomain.from_db(address)
        return ResponseSuccess(address_obj)

    def update_address(self, data):
        user_email = request.args["user_email"]
        exist_user = self.session.query(UserTable).filter(UserTable.email==user_email).first()
        id = data.pop("id")
        address = self.session.query(AddressTable)\
                    .join(UserTable)\
                            .filter(and_(
                                    AddressTable.id == id,
                                    or_(
                                        UserTable.email == user_email,
                                        exist_user.is_admin==True
                                    )
                                )
                            ).first()
        if(address is None):
            return ResponseFailure(
                type_=ResponseTypes.BADREQUEST_ERROR,
                message="No address found for this id!"
            )
        for key, value in data.items():
            setattr(address, key, value)

        address_obj = AddressDomain.from_db(address)

        self.session.commit()
        return ResponseSuccess({
            "message": "Update address successfully",
            "data": address_obj
        })

    def delete_address(self, id):
        user_email = request.args["user_email"]
        exist_user = self.session.query(UserTable).filter(UserTable.email==user_email).first()

        address = self.session.query(AddressTable)\
                        .join(UserTable)\
                            .filter(and_(
                                    AddressTable.id == id,
                                    or_(
                                        UserTable.email == user_email,
                                        exist_user.is_admin==True
                                    )
                                )
                            ).first()
        if(address is None):
            return ResponseFailure(
                type_=ResponseTypes.BADREQUEST_ERROR,
                message="No address found for this id!"
            )
        self.session.delete(address)
        self.session.commit()
        return ResponseSuccess(
            value={
                "message": "delete address successfully"
            })
