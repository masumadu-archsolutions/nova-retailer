import os

import jwt
import inspect
from functools import wraps
from flask import request
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError, PyJWTError

import config
from core.exceptions import AppException


def auth_required(authorized_roles=None):
    def authorize_user(func):
        """
        A wrapper to authorize an action using
        :param func: {function}` the function to wrap around
        :return:
        """

        @wraps(func)
        def view_wrapper(*args, **kwargs):
            authorization_header = request.headers.get("Authorization")
            if not authorization_header:
                raise AppException.Unauthorized("Missing authentication token")

            token = authorization_header.split()[1]
            try:
                key = os.getenv("JWT_PUBLIC_KEY")  # noqa E501
                payload = jwt.decode(
                    token,
                    key=key,
                    algorithms=config.Config.JWT_ALGORITHMS,
                    # algorithms=["HS256", "RS256"],
                    audience="account",
                    issuer=config.Config.JWT_ISSUER,
                )  # noqa E501
                # Get retailer roles from token
                token_role = payload.get("resource_access").get("nova_retailer")
                retailer_role = token_role.get("roles")

                if authorized_roles:
                    resource_access_role = authorized_roles.split("|")
                    if is_authorized(retailer_role, resource_access_role):
                        if "user_id" in inspect.getfullargspec(func).args:
                            kwargs["user_id"] = payload.get(
                                "preferred_username"
                            )  # noqa E501
                        return func(*args, **kwargs)
                else:
                    if "user_id" in inspect.getfullargspec(func).args:
                        kwargs["user_id"] = payload.get(
                            "preferred_username"
                        )  # noqa E501
                    return func(*args, **kwargs)
            except ExpiredSignatureError as e:
                raise AppException.ExpiredTokenException(context=e.args)
            except InvalidTokenError as e:
                raise AppException.OperationError(context=e.args)
            except PyJWTError as e:
                raise AppException.OperationError(context=e.args)
            raise AppException.Unauthorized(context="operation unauthorized")

        return view_wrapper

    return authorize_user


def is_authorized(retailer_role, resource_role):
    for role in retailer_role:
        if role in resource_role:
            return True

    return False
