import copy
from datetime import datetime, timedelta
import sys
import jwt
import os
from flask import current_app, request
from app.core.error.response import ResponseSuccess, ResponseFailure, ResponseTypes
from app.core.db.postgres_configuration import PostgresConfiguration, UserTable
from werkzeug.security import generate_password_hash, check_password_hash
from app.ecommerce.user.domain.user_domain import UserDomain

class UserRepository():
    def __init__(self):
        self.session = PostgresConfiguration.get_session()

    def user_sign_up(self, data):
        exists_user = self.session.query(UserTable).filter_by(
            email=data["email"]
        ).first()
        
        user_data = copy.deepcopy(data)
        if exists_user is None:
            password = user_data.pop("password")
            new_user = UserTable(**user_data)
            new_user.password = generate_password_hash(password=password)
            self.session.add(new_user)
            self.session.commit()
            return ResponseSuccess({
                "message": "User created successfully",
                "data": UserDomain.from_db(new_user)
            })
        else:
            return ResponseFailure(
                type_=ResponseTypes.BADREQUEST_ERROR,
                message="Email is already registered"
            )

    def user_login(self, data):
        exists_user = self.session.query(UserTable).filter_by(
            email=data["email"]
        ).first()
        if exists_user is None or not exists_user.is_active:
            return ResponseFailure(
                type_=ResponseTypes.BADREQUEST_ERROR,
                message="No user found for this email!"
            )
        elif not check_password_hash(exists_user.password, data["password"]):
            return ResponseFailure(
                type_=ResponseTypes.BADREQUEST_ERROR,
                message="password does not match"
            )
        else:
            token = jwt.encode(
                payload={"user_email": exists_user.email,'exp':datetime.utcnow() + timedelta(days=int(current_app.config["JWT_EXP_TIME_DAYS"]))},
                key=current_app.config["SECRET_KEY"],
                algorithm=current_app.config["JWT_HASH_METHOD"],
            )
            res = UserDomain.from_db(exists_user)
            return ResponseSuccess({"token": token, "data": res})

    def user_update_profile(self, data):
        if "id" in data:
            exists_user = self.session.query(UserTable).filter_by(
                id=data["id"]
            ).first()
            if exists_user is None or exists_user.is_delete:
                return ResponseFailure(
                    ResponseTypes.SUCCESS,
                    {
                        "message": "No user found for this id!"
                    }
                )
        else:
            user_email = request.args["user_email"]
            exists_user = self.session.query(UserTable).filter_by(
                email=user_email
            ).first()
        for key, value in data.items():
            setattr(exists_user, key, value)

        exists_user.updated_at = datetime.now()
        user_obj = UserDomain.from_db(exists_user)

        self.session.commit()
        return ResponseSuccess({
            "message": "Update user successfully",
            "data": user_obj
        })

    def user_profile(self):
        user_email = request.args["user_email"]
        exists_user = self.session.query(UserTable).filter_by(
            email=user_email
        ).first()
        user_obj = UserDomain.from_db(exists_user)
        return ResponseSuccess(user_obj)

    def user_get_all_users(self):
        users = self.session.query(UserTable).all()
        result = [UserDomain.from_db(i) for i in users]
        return ResponseSuccess(result)

    def user_get_by_id(self, id):
        user = self.session.query(UserTable).filter_by(id=id).first()
        if user is None or user.is_delete:
            return ResponseFailure(
                ResponseTypes.SUCCESS,
                {
                    "message": "No user found for this id!"
                }
            )
        user_obj = UserDomain.from_db(user)
        return ResponseSuccess(user_obj)

    def user_delete(self, id):
        user = self.session.query(UserTable).filter_by(id=id).first()
        if user is None or user.is_delete:
            return ResponseFailure(
                type_=ResponseTypes.SUCCESS,
                message="No user found for this id!",
                errors=[]
            )
        user.is_delete = True
        user.is_active = False
        self.session.commit()

        return ResponseSuccess(value={"message": "Delete user successfully"})
