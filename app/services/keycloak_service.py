import os

import requests
from requests import exceptions
import config
from dataclasses import dataclass
from app import constants
from core.exceptions import AppException
from core.service_interfaces.auth_service_interface import (
    AuthServiceInterface,
)
import jwt
from jwt import exceptions as jwt_exceptions

CLIENT_ID = config.Config.KEYCLOAK_CLIENT_ID or ""
CLIENT_SECRET = config.Config.KEYCLOAK_CLIENT_SECRET or ""
URI = config.Config.KEYCLOAK_URI or ""
ADMIN_REALM = config.Config.KEYCLOAK_ADMIN_REALM or ""
REALM = config.Config.KEYCLOAK_REALM or ""
REALM_PREFIX = "/auth/realms/"
AUTH_ENDPOINT = "/protocol/openid-connect/token/"
REALM_URL = "/auth/admin/realms/"
OPENID_CONFIGURATION_ENDPOINT = "/.well-known/openid-configuration"


@dataclass
class AuthService(AuthServiceInterface):
    """
    This class is an intermediary between this service and the IAM service i.e Keycloak.
    It makes authentication and authorization api calls to the IAM service on
    behalf of the application. Use this class when authenticating an entity
    """

    headers = None
    refresh_token = None
    roles = []

    def get_token(self, request_data):
        """
        Login to keycloak and return token
        :param request_data: {dict} a dictionary containing username and password
        :return: {dict} a dictionary containing token and refresh token
        """
        data = {
            "grant_type": "password",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "username": request_data.get("username"),
            "password": request_data.get("password"),
        }

        # create keycloak uri for token login
        url = URI + REALM_PREFIX + REALM + AUTH_ENDPOINT

        keycloak_response = self.send_request_to_keycloak(
            method="post", url=url, data=data
        )

        if keycloak_response.status_code != 200:
            raise AppException.KeyCloakAdminException(
                {constants.KEYCLOAK_ACCESS_TOKEN: [keycloak_response.json()]},
                status_code=keycloak_response.status_code,
            )

        tokens_data: dict = keycloak_response.json()
        result = {
            "access_token": tokens_data.get("access_token"),
            "refresh_token": tokens_data.get("refresh_token"),
        }

        return result

    def token_refresh(self, refresh_token):
        """
        :param refresh_token: a {str} containing the refresh token
        :return: {dict} a dictionary containing the token and refresh token
        """

        request_data = {
            "grant_type": "refresh_token",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "refresh_token": refresh_token,
        }
        url = URI + REALM_PREFIX + REALM + AUTH_ENDPOINT
        keycloak_response = self.send_request_to_keycloak(
            method="post", url=url, data=request_data
        )

        if keycloak_response.status_code != requests.codes.ok:
            raise AppException.KeyCloakAdminException(
                {constants.KEYCLOAK_REFRESH_TOKEN: [keycloak_response.json()]},
                status_code=keycloak_response.status_code,
            )

        data: dict = keycloak_response.json()
        return {
            "access_token": data.get("access_token"),
            "refresh_token": data.get("refresh_token"),
        }

    def create_user(self, request_data: dict):
        data = {
            "email": request_data.get("email"),
            "username": request_data.get("username"),
            "firstName": request_data.get("first_name"),
            "lastName": request_data.get("last_name"),
            "attributes": {
                "phone_number": request_data.get("phone_number"),
                "id_type": request_data.get("id_type"),
                "id_number": request_data.get("id_number"),
                "status": request_data.get("status"),
            },
            "credentials": [
                {
                    "value": request_data.get("password"),
                    "type": "password",
                    "temporary": False,
                }
            ],
            "enabled": True,
            "emailVerified": True,
            "access": {
                "manageGroupMembership": True,
                "view": True,
                "mapRoles": True,
                "impersonate": True,
                "manage": True,
            },
        }

        endpoint: str = "/users"
        # create user
        self.keycloak_post(endpoint, data)
        # get user details from keycloak
        user = self.get_keycloak_user(request_data.get("username"))
        user_id: str = user.get("id")

        # assign user to group
        group = request_data.get("group")
        iam_groups = self.get_all_groups()
        required_groups = list(filter(lambda x: x.get("name") == group, iam_groups))
        if len(required_groups) == 0:
            raise AppException.OperationError(
                f"group {group} does not exist in IAM service"
            )
        group_data = required_groups[0]
        # assign user to a group
        self.assign_group(user_id, group_data)
        return user.get("username")

    def update_user(self, request_data: dict):
        user = self.get_keycloak_user(request_data.get("username"))
        data = {
            "firstName": request_data.get("first_name"),
            "lastName": request_data.get("last_name"),
            "attributes": {
                "phone_number": request_data.get("phone_number"),
                "id_type": request_data.get("id_type"),
                "id_number": request_data.get("id_number"),
                "status": request_data.get("status"),
            },
        }
        endpoint: str = f"/users/{user.get('id')}"
        # update user
        self.keycloak_put(endpoint, data)
        # get user details from keycloak
        updated_user = self.get_keycloak_user(request_data.get("username"))
        return updated_user.get("username")

    def get_all_groups(self):
        url = URI + REALM_URL + REALM + "/groups"
        keycloak_response = self.send_request_to_keycloak(
            method="get", url=url, headers=self.get_keycloak_headers()
        )

        if keycloak_response.status_code >= 300:
            raise AppException.KeyCloakAdminException(
                {constants.KEYCLOAK_GROUP: [keycloak_response.json()]},
                status_code=keycloak_response.status_code,
            )
        return keycloak_response.json()

    def get_keycloak_user(self, username):
        """

        :param username: username of keycloak user which is normally the uuid
        of the user in the database
        :return:
        """
        url = URI + REALM_URL + REALM + "/users?username=" + username
        keycloak_response = self.send_request_to_keycloak(
            method="get", url=url, headers=self.get_keycloak_headers()
        )
        if keycloak_response.status_code != 200:
            raise AppException.KeyCloakAdminException(
                {constants.KEYCLOAK_USER: [keycloak_response.json()]},
                status_code=keycloak_response.status_code,
            )
        user = keycloak_response.json()
        if len(user) == 0:
            return None
        else:
            return user[0]

    def assign_group(self, user_id, group):
        endpoint = "/users/" + user_id + "/groups/" + group.get("id")
        url = URI + REALM_URL + REALM + endpoint
        keycloak_response = self.send_request_to_keycloak(
            method="put", url=url, headers=self.get_keycloak_headers()
        )

        if keycloak_response.status_code >= 300:
            raise AppException.KeyCloakAdminException(
                {constants.KEYCLOAK_GROUP: [keycloak_response.json()]},
                status_code=keycloak_response.status_code,
            )
        return True

    def reset_password(self, data):
        user_id = data.get("user_id")
        new_password = data.get("new_password")
        url = "/users/" + user_id + "/reset-password"

        data = {"type": "password", "value": new_password, "temporary": False}

        self.keycloak_put(url, data)
        return True

    def keycloak_post(self, endpoint, data):
        """
        Make a POST request to Keycloak
        :param {string} endpoint Keycloak endpoint
        :data {object} data Keycloak data object
        :return {Response} request response object
        """
        url = URI + REALM_URL + REALM + endpoint
        headers = self.get_keycloak_headers()
        keycloak_response = requests.post(url, data=data, headers=headers)
        keycloak_response = self.send_request_to_keycloak(
            method="post", url=url, headers=headers, json=data
        )
        if keycloak_response.status_code >= 300:
            raise AppException.KeyCloakAdminException(
                {constants.KEYCLOAK_POST: [keycloak_response.json()]},
                status_code=keycloak_response.status_code,
            )
        return keycloak_response

    def keycloak_put(self, endpoint, data):
        """
        Make a POST request to Keycloak
        :param {string} endpoint Keycloak endpoint
        :data {object} data Keycloak data object
        :return {Response} request response object
        """
        url = URI + REALM_URL + REALM + endpoint
        keycloak_response = self.send_request_to_keycloak(
            method="put", url=url, headers=self.get_keycloak_headers(), json=data
        )

        if keycloak_response.status_code >= 300:
            raise AppException.KeyCloakAdminException(
                {constants.KEYCLOAK_PUT: [keycloak_response.json()]},
                status_code=keycloak_response.status_code,
            )
        return keycloak_response

    # noinspection PyMethodMayBeStatic
    def get_admin_token(self):
        """
        :returns {string} Keycloak admin user access_token
        """
        data = {
            "grant_type": "password",
            "client_id": "admin-cli",
            "username": config.Config.KEYCLOAK_ADMIN_USER,
            "password": config.Config.KEYCLOAK_ADMIN_PASSWORD,
        }

        url = URI + REALM_PREFIX + ADMIN_REALM + AUTH_ENDPOINT
        keycloak_response = self.send_request_to_keycloak(
            method="post", url=url, data=data
        )
        if keycloak_response.status_code != requests.codes.ok:
            raise AppException.KeyCloakAdminException(
                {constants.KEYCLOAK_ERROR: [keycloak_response.json()]}, status_code=500
            )
        data = keycloak_response.json()
        return data

    # noinspection PyMethodMayBeStatic
    def refresh_admin_token(self, refresh_token):
        """
        :returns {string} Keycloak admin user refresh_token
        """
        request_data = {
            "grant_type": "refresh_token",
            "client_id": "admin-cli",
            "refresh_token": refresh_token,
        }

        url = URI + REALM_PREFIX + ADMIN_REALM + AUTH_ENDPOINT
        keycloak_response = self.send_request_to_keycloak(
            method="post", url=url, data=request_data
        )

        if keycloak_response.status_code != requests.codes.ok:
            raise AppException.KeyCloakAdminException(
                {constants.KEYCLOAK_ERROR: [keycloak_response.json()]}, status_code=500
            )
        data = keycloak_response.json()
        return data

    def get_keycloak_headers(self):
        """
        login as an admin user into keycloak and use the access token as an
        authentication user.
        :return {object}  Object of keycloak headers
        """
        if self.headers:
            header_token = self.headers.get("Authorization").split()[1]
            if self.decode_header_token(header_token):
                return self.headers
            else:
                new_token = self.refresh_admin_token(self.refresh_token)
                headers = {
                    "Authorization": "Bearer " + new_token.get("access_token"),
                    "Content-Type": "application/json",
                }
                self.headers = headers
                self.refresh_token = new_token.get("refresh_token")
                return self.headers
        else:
            token = self.get_admin_token()
            headers = {
                "Authorization": "Bearer " + token.get("access_token"),
                "Content-Type": "application/json",
            }
            self.headers = headers
            self.refresh_token = token.get("refresh_token")

            return headers

    def decode_header_token(self, token):
        admin_endpoints = self.admin_openid_configuration()
        try:
            jwt.decode(
                token,
                algorithms=["HS256", "RS256"],
                key=os.getenv("JWT_PUBLIC_KEY"),
                issuer=admin_endpoints.get("issuer"),
            )  # noqa E501
            return True
        except jwt_exceptions.ExpiredSignatureError:
            return False
        except jwt_exceptions.InvalidTokenError as e:
            raise AppException.KeyCloakAdminException(context=e.args)

    def admin_openid_configuration(self):
        url = URI + REALM_PREFIX + ADMIN_REALM + OPENID_CONFIGURATION_ENDPOINT
        keycloak_response = self.send_request_to_keycloak(method="get", url=url)

        # handle keycloak response
        if keycloak_response.status_code != requests.codes.ok:
            raise AppException.KeyCloakAdminException(
                {constants.KEYCLOAK_ERROR: [keycloak_response.json()]}, status_code=500
            )
        data = keycloak_response.json()
        return data

    def realm_openid_configuration(self):
        url = URI + REALM_PREFIX + REALM + OPENID_CONFIGURATION_ENDPOINT
        keycloak_response = self.send_request_to_keycloak(method="get", url=url)

        # handle keycloak response
        if keycloak_response.status_code != requests.codes.ok:
            raise AppException.KeyCloakAdminException(
                {constants.KEYCLOAK_ERROR: [keycloak_response.json()]}, status_code=500
            )
        data = keycloak_response.json()
        return data

    # noinspection PyMethodMayBeStatic
    def send_request_to_keycloak(
        self, method=None, url=None, headers=None, json=None, data=None
    ):
        try:
            response = requests.request(
                method=method, url=url, headers=headers, json=json, data=data
            )
        except exceptions.ConnectionError:
            raise AppException.OperationError(
                context=constants.KEYCLOAK_CONNECTION_ERROR
            )
        except exceptions.HTTPError:
            raise AppException.OperationError(context=constants.KEYCLOAK_HTTP_ERROR)
        except exceptions.Timeout:
            raise AppException.OperationError(
                context=constants.KEYCLOAK_CONNECTION_TIMEOUT
            )
        except exceptions.RequestException:
            raise AppException.OperationError(context=constants.KEYCLOAK_REQUEST_ERROR)
        return response
