from functools import wraps
import json
import os
from flask import Response, current_app
import jwt
from flask import request
from app.ecommerce.user.domain.user_domain import UserDomain
from app.core.db.postgres_configuration import PostgresConfiguration, UserTable
from app.ecommerce.user.repository.user_repository import UserRepository
from app.core.error.response import STATUS_CODES, ResponseFailure, ResponseTypes

session = PostgresConfiguration.get_session()

def check_token_and_get_user():
    if 'Authorization' not in request.headers:
        raise jwt.InvalidSignatureError("Authentication Token is missing!")

    token = request.headers["Authorization"]
    data = jwt.decode(
        token, current_app.config["SECRET_KEY"],
        algorithms=["HS256"]
    )
    if "user_email" not in data:
        raise jwt.InvalidSignatureError("Invalid Authentication token!")
    exists_user = session.query(UserTable).filter_by(
        email=data["user_email"]
    ).first()
    if exists_user is None or not exists_user.is_active:
        raise jwt.InvalidSignatureError("Account should be deleted!")

    return exists_user


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            exists_user = check_token_and_get_user()
            http_args = request.args.to_dict()
            http_args['user_email'] = exists_user.email
            request.args = http_args
        except Exception as exec:
            res = ResponseFailure(
                ResponseTypes.UNAUTHORIZED,
                exec
            )
            return Response(
                json.dumps(res.value),
                mimetype="application/json",
                status=STATUS_CODES[res.type],
            )
        return f(*args, **kwargs)
    return decorated


def admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            exists_user = check_token_and_get_user()
            if not exists_user.is_admin:
                res = ResponseFailure(
                    type_=ResponseTypes.UNAUTHORIZED,
                    message="Unauthorized account to access"
                )
                return Response(
                    json.dumps(res.value),
                    mimetype="application/json",
                    status=STATUS_CODES[res.type],
                )
            else:                
                http_args = request.args.to_dict()
                http_args['user_email'] = exists_user.email
                request.args = http_args

        except Exception as exec:
            res = ResponseFailure(
                type_=ResponseTypes.UNAUTHORIZED,
                message=exec
            )
            return Response(
                json.dumps(res.value),
                mimetype="application/json",
                status=STATUS_CODES[res.type],
            )
        return f(*args, **kwargs)
    return decorated
