import os
import json
import requests
from app.definitions.exceptions.app_exceptions import AppException
from app.definitions.service_interfaces.auth_service_interface import (
    AuthServiceInterface,
)
from flask import current_app as app


class AuthService(AuthServiceInterface):
    def get_token(self, request_data):

        data = {
            "grant_type": "password",
            "client_id": os.getenv("KEYCLOAK_CLIENT_ID"),
            "client_secret": os.getenv("KEYCLOAK_CLIENT_SECRET"),
            "username": request_data.get("username"),
            "password": request_data.get("password"),
        }

        url = "".join(
            [
                os.getenv("KEYCLOAK_URI"),
                "/auth/realms/",
                os.getenv("KEYCLOAK_REALM"),
                "/protocol/openid-connect/token",
            ]
        )

        response = requests.post(url, data=data)
        if response.status_code != 200:
            raise AppException.KeyCloakAdminException(
                context={"message": "Error in username or password"},
                status_code=response.status_code,
            )
        tokens_data = response.json()
        result = {
            "access_token": tokens_data["access_token"],
            "refresh_token": tokens_data["refresh_token"],
        }

        return result

    def refresh_token(self, refresh_token):
        request_data = {
            "grant_type": "refresh_token",
            "client_id": os.getenv("KEYCLOAK_CLIENT_ID"),
            "client_secret": os.getenv("KEYCLOAK_CLIENT_SECRET"),
            "refresh_token": refresh_token,
        }

        url = "".join(
            [
                os.getenv("KEYCLOAK_URI"),
                "/auth/realms/",
                os.getenv("KEYCLOAK_REALM"),
                "/protocol/openid-connect/token",
            ]
        )

        response = requests.post(url, data=request_data)

        if response.status_code != requests.codes.ok:

            raise AppException.BadRequest(context={
                "errorMessage": "Error in refresh token"
            })

        data = response.json()
        return {
            "access_token": data["access_token"],
            "refresh_token": data["refresh_token"],
        }

    def create_user(self, request_data):
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
            "emailVerified": False,
        }

        endpoint = "/users"
        self.keycloak_post(endpoint, data)
        return True

    def keycloak_post(self, endpoint, data):
        """
        Make a POST request to Keycloak
        :param {string} endpoint Keycloak endpoint
        :data {object} data Keycloak data object
        :return {Response} request response object
        """
        url = (
            os.getenv("KEYCLOAK_URI")
            + "/auth/admin/realms/"
            + os.getenv("KEYCLOAK_REALM")
            + endpoint
        )
        headers = self.get_keycloak_headers()
        response = requests.post(url, headers=headers, json=data)
        if response.status_code >= 300:
            # app.logger.error(response.text)
            raise AppException.KeyCloakAdminException(
                context={"message": response.json().get("errorMessage")},
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
            "username": os.getenv("KEYCLOAK_ADMIN_USER"),
            "password": os.getenv("KEYCLOAK_ADMIN_PASSWORD"),
        }

        url = "".join(
            [
                os.getenv("KEYCLOAK_URI"),
                "/auth/realms/",
                os.getenv("KEYCLOAK_REALM"),
                "/protocol/openid-connect/token",
            ]
        )
        response = requests.post(
            url,
            data=data,
        )
        if response.status_code != requests.codes.ok:
            raise AppException.KeyCloakAdminException(
                context={"response": response.text}, status_code=500
            )
        data = response.json()
        return data.get("access_token")

    def get_keycloak_headers(self):
        """

        :return {object}  Object of keycloak headers
        """
        return {
            "Authorization": "Bearer " + self.get_keycloak_access_token(),
            "Content-Type": "application/json",
        }
