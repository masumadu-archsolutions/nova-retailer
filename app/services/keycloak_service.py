import json
import requests
from requests import exceptions
import config
from dataclasses import dataclass
from app import constants
from core.exceptions import AppException
from core.service_interfaces.auth_service_interface import (
    AuthServiceInterface,
)

CLIENT_ID = config.Config.KEYCLOAK_CLIENT_ID or ""
CLIENT_SECRET = config.Config.KEYCLOAK_CLIENT_SECRET or ""
URI = config.Config.KEYCLOAK_URI or ""
ADMIN_REALM = config.Config.KEYCLOAK_ADMIN_REALM or ""
REALM = config.Config.KEYCLOAK_REALM or ""
REALM_PREFIX = "/auth/realms/"
AUTH_ENDPOINT = "/protocol/openid-connect/token/"
REALM_URL = "/auth/admin/realms/"


@dataclass
class AuthService(AuthServiceInterface):
    """
    This class is an intermediary between this service and the IAM service i.e Keycloak.
    It makes authentication and authorization api calls to the IAM service on
    behalf of the application. Use this class when authenticating an entity
    """

    headers = None
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
        # send post request to keycloak server
        try:
            response = requests.post(url, data=data)
        except exceptions.ConnectionError:
            raise AppException.OperationError(
                context=constants.KEYCLOAK_CONNECTION_ERROR
            )
        except exceptions.HTTPError:
            raise AppException.OperationError(
                context=constants.KEYCLOAK_HTTP_ERROR
            )
        except exceptions.Timeout:
            raise AppException.OperationError(
                context=constants.KEYCLOAK_CONNECTION_TIMEOUT
            )
        except exceptions.RequestException:
            raise AppException.OperationError(
                context=constants.KEYCLOAK_REQUEST_ERROR
            )

        # handle response sent by keycloak server
        if response.status_code != 200:
            raise AppException.KeyCloakAdminException(
                {constants.KEYCLOAK_ACCESS_TOKEN: [response.json()]},
                status_code=response.status_code,
            )

        tokens_data: dict = response.json()
        result = {
            "access_token": tokens_data.get("access_token"),
            "refresh_token": tokens_data.get("refresh_token"),
        }

        return result

    def refresh_token(self, refresh_token):
        """

        :param refresh_token: a {str} containing the refresh token
        :return: {dict} a dictionary containing the token and refresh token
        """
        assert refresh_token, "refresh token cannot be None"

        request_data = {
            "grant_type": "refresh_token",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "refresh_token": refresh_token,
        }

        url = URI + REALM_PREFIX + REALM + AUTH_ENDPOINT
        # send post request to keycloak server
        try:
            response = requests.post(url, data=request_data)
        except exceptions.ConnectionError:
            raise AppException.OperationError(
                context=constants.KEYCLOAK_CONNECTION_ERROR
            )
        except exceptions.HTTPError:
            raise AppException.OperationError(
                context=constants.KEYCLOAK_HTTP_ERROR
            )
        except exceptions.Timeout:
            raise AppException.OperationError(
                context=constants.KEYCLOAK_CONNECTION_TIMEOUT
            )
        except exceptions.RequestException:
            raise AppException.OperationError(
                context=constants.KEYCLOAK_REQUEST_ERROR
            )

        # handle response sent by keycloak server
        if response.status_code != requests.codes.ok:
            raise AppException.KeyCloakAdminException(
                {constants.KEYCLOAK_REFRESH_TOKEN: [response.json()]},
                status_code=response.status_code,
            )

        data: dict = response.json()
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

    def get_all_groups(self):
        url = URI + REALM_URL + REALM + "/groups"
        # send get request to keycloak server
        try:
            response = requests.get(url, headers=self.get_keycloak_headers())
        except exceptions.ConnectionError:
            raise AppException.OperationError(
                context=constants.KEYCLOAK_CONNECTION_ERROR
            )
        except exceptions.HTTPError:
            raise AppException.OperationError(
                context=constants.KEYCLOAK_HTTP_ERROR
            )
        except exceptions.Timeout:
            raise AppException.OperationError(
                context=constants.KEYCLOAK_CONNECTION_TIMEOUT
            )
        except exceptions.RequestException:
            raise AppException.OperationError(
                context=constants.KEYCLOAK_REQUEST_ERROR
            )
        # handle response sent by keycloak server
        if response.status_code >= 300:
            raise AppException.KeyCloakAdminException(
                {constants.KEYCLOAK_GROUP: [response.json()]},
                status_code=response.status_code,
            )
        return response.json()

    def get_keycloak_user(self, username):
        """

        :param username: username of keycloak user which is normally the uuid
        of the user in the database
        :return:
        """
        url = URI + REALM_URL + REALM + "/users?username=" + username
        # send a get request to keycloak server
        try:
            response = requests.get(url, headers=self.get_keycloak_headers())
        except exceptions.ConnectionError:
            raise AppException.OperationError(
                context=constants.KEYCLOAK_CONNECTION_ERROR
            )
        except exceptions.HTTPError:
            raise AppException.OperationError(
                context=constants.KEYCLOAK_HTTP_ERROR
            )
        except exceptions.Timeout:
            raise AppException.OperationError(
                context=constants.KEYCLOAK_CONNECTION_TIMEOUT
            )
        except exceptions.RequestException:
            raise AppException.OperationError(
                context=constants.KEYCLOAK_REQUEST_ERROR
            )
        # handle response sent by keycloak server
        if response.status_code != 200:
            raise AppException.KeyCloakAdminException(
                {constants.KEYCLOAK_USER: [response.json()]},
                status_code=response.status_code,
            )
        user = response.json()
        if len(user) == 0:
            return None
        else:
            return user[0]

    def assign_group(self, user_id, group):
        endpoint = "/users/" + user_id + "/groups/" + group.get("id")
        url = URI + REALM_URL + REALM + endpoint
        headers = self.headers or self.get_keycloak_headers()
        # send a put request to keycloak server
        try:
            response = requests.put(url, headers=headers)
        except exceptions.ConnectionError:
            raise AppException.OperationError(
                context=constants.KEYCLOAK_CONNECTION_ERROR
            )
        except exceptions.HTTPError:
            raise AppException.OperationError(
                context=constants.KEYCLOAK_HTTP_ERROR
            )
        except exceptions.Timeout:
            raise AppException.OperationError(
                context=constants.KEYCLOAK_CONNECTION_TIMEOUT
            )
        except exceptions.RequestException:
            raise AppException.OperationError(
                context=constants.KEYCLOAK_REQUEST_ERROR
            )
        # handle response sent by keycloak server
        if response.status_code >= 300:
            raise AppException.KeyCloakAdminException(
                {constants.KEYCLOAK_GROUP: [response.json()]},
                status_code=response.status_code,
            )
        return True

    def reset_password(self, data):
        user_id = data.get("user_id")
        new_password = data.get("new_password")
        # assert user_id, "user_id is required"
        # assert new_password, "new_password is required"
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
        headers = self.headers or self.get_keycloak_headers()
        # send a post request to keycloak server
        try:
            response = requests.post(url, headers=headers, json=data)
        except exceptions.ConnectionError:
            raise AppException.OperationError(
                context=constants.KEYCLOAK_CONNECTION_ERROR
            )
        except exceptions.HTTPError:
            raise AppException.OperationError(
                context=constants.KEYCLOAK_HTTP_ERROR
            )
        except exceptions.Timeout:
            raise AppException.OperationError(
                context=constants.KEYCLOAK_CONNECTION_TIMEOUT
            )
        except exceptions.RequestException:
            raise AppException.OperationError(
                context=constants.KEYCLOAK_REQUEST_ERROR
            )
        # handle response from keycloak server
        if response.status_code >= 300:
            raise AppException.KeyCloakAdminException(
                {constants.KEYCLOAK_POST: [response.json()]},
                status_code=response.status_code,
            )
        return response

    def keycloak_put(self, endpoint, data):
        """
        Make a POST request to Keycloak
        :param {string} endpoint Keycloak endpoint
        :data {object} data Keycloak data object
        :return {Response} request response object
        """
        url = URI + REALM_URL + REALM + endpoint
        headers = self.headers or self.get_keycloak_headers()
        # send a put request to keycloak server
        try:
            response = requests.put(url, headers=headers, json=data)
        except exceptions.ConnectionError:
            raise AppException.OperationError(
                context=constants.KEYCLOAK_CONNECTION_ERROR
            )
        except exceptions.HTTPError:
            raise AppException.OperationError(
                context=constants.KEYCLOAK_HTTP_ERROR
            )
        except exceptions.Timeout:
            raise AppException.OperationError(
                context=constants.KEYCLOAK_CONNECTION_TIMEOUT
            )
        except exceptions.RequestException:
            raise AppException.OperationError(
                context=constants.KEYCLOAK_REQUEST_ERROR
            )
        # handle response from keycloak server
        if response.status_code >= 300:
            raise AppException.KeyCloakAdminException(
                {constants.KEYCLOAK_PUT: [response.json()]},
                status_code=response.status_code,
            )
        return response

    # noinspection PyMethodMayBeStatic
    def get_keycloak_access_token(self):
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
        try:
            response = requests.post(url, data=data)
        except exceptions.ConnectionError:
            raise AppException.OperationError(
                context=constants.KEYCLOAK_CONNECTION_ERROR
            )
        except exceptions.HTTPError:
            raise AppException.OperationError(
                context=constants.KEYCLOAK_HTTP_ERROR
            )
        except exceptions.Timeout:
            raise AppException.OperationError(
                context=constants.KEYCLOAK_CONNECTION_TIMEOUT
            )
        except exceptions.RequestException:
            raise AppException.OperationError(
                context=constants.KEYCLOAK_REQUEST_ERROR
            )
        if response.status_code != requests.codes.ok:
            raise AppException.KeyCloakAdminException(
                {constants.KEYCLOAK_ERROR: [response.json()]},
                status_code=500
            )
        data = response.json()
        return data.get("access_token")

    def get_keycloak_headers(self):
        """
        login as an admin user into keycloak and use the access token as an
        authentication user.
        :return {object}  Object of keycloak headers
        """

        if self.headers:
            return self.headers

        headers = {
            "Authorization": "Bearer " + self.get_keycloak_access_token(),
            "Content-Type": "application/json",
        }
        self.headers = headers
        return headers
