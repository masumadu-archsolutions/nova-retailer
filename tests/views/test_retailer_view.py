# import uuid
import unittest

# from core.exceptions import AppException
from tests.utils.base_test_case import BaseTestCase
from flask import url_for
import pytest
from unittest import mock
from app.services import AuthService

# from tests import MockAuthService
from app.models import RetailerModel


class TestRetailerRoutes(BaseTestCase):
    @pytest.mark.retailer_view
    @mock.patch.object(AuthService, "create_user")
    def test_create_retailer(self, mock_create_user):
        mock_create_user.return_value = self.auth_service.create_user(
            self.create_retailer
        )
        with self.client:
            response = self.client.post(
                url_for("retailer.create_retailer"), json=self.create_retailer
            )
            response_data = response.json
            self.assertStatus(response, 201)
            self.assertIsInstance(response_data, dict)
            self.assertEqual(len(response_data), 1)
            self.assertIn("id", response_data)

    @pytest.mark.retailer_view
    @mock.patch.object(AuthService, "get_token")
    def test_login_retailer(self, mock_get_token):
        mock_get_token.return_value = self.auth_service.get_token(
            self.retailer_credentials
        )
        with self.client:
            response = self.client.post(
                url_for("retailer.login_retailer"), json=self.retailer_credentials
            )
            response_data = response.json
            self.assert200(response)
            self.assertIsInstance(response_data, dict)
            self.assertEqual(len(response_data), 2)
            self.assertIn("access_token", response_data)
            self.assertIn("refresh_token", response_data)

    @pytest.mark.retailer_view
    @mock.patch("core.utils.auth.jwt.decode")
    def test_find_by_id(self, mock_jwt_decode):
        mock_jwt_decode.return_value = self.required_roles
        with self.client:
            self.assertEqual(RetailerModel.query.count(), 1)
            retailer = RetailerModel.query.filter_by(
                phone_number=self.existing_retailer.get("phone_number")
            ).first()
            self.assertIsInstance(retailer, RetailerModel)
            self.assertIsNotNone(retailer.id)
            response = self.client.get(
                url_for("retailer.find_retailer", retailer_id=retailer.id),
                headers=self.headers,
            )
            response_data = response.json
            self.assertStatus(response, 200)
            self.assertIsInstance(response_data, dict)
            self.assertIsNotNone(response_data.get("id"))
            self.assertNotIn("pin", response_data)
            self.assertEqual(
                self.existing_retailer.get("phone_number"),
                response_data.get("phone_number"),
            )

    @pytest.mark.retailer_view
    @mock.patch.object(AuthService, "update_user")
    @mock.patch("core.utils.auth.jwt.decode")
    def test_update_by_id(self, mock_jwt_decode, mock_update_user):
        mock_jwt_decode.return_value = self.required_roles
        mock_update_user.return_value = self.auth_service.update_user(
            self.update_retailer
        )
        with self.client:
            self.assertEqual(RetailerModel.query.count(), 1)
            retailer = RetailerModel.query.filter_by(
                phone_number=self.existing_retailer.get("phone_number")
            ).first()
            self.assertIsInstance(retailer, RetailerModel)
            self.assertIsNotNone(retailer.id)
            response = self.client.patch(
                url_for("retailer.update_retailer", retailer_id=retailer.id),
                json=self.update_retailer,
                headers=self.headers,
            )
            response_data = response.json
            self.assertStatus(response, 200)
            self.assertIsInstance(response_data, dict)
            self.assertIsNotNone(response_data.get("id"))
            self.assertNotIn("pin", response_data)
            self.assertNotEqual(
                response_data.get("phone_number"),
                self.existing_retailer.get("phone_number"),
            )
            self.assertEqual(
                response_data.get("phone_number"),
                self.update_retailer.get("phone_number"),
            )


if __name__ == "__main__":
    unittest.main()
    #     data = response.json
    #
    #     self.assertEqual(
    #         data.get("first_name"), self.customer_data.get("first_name")
    #     )
    # find_admin_by_id = AdminController(
    #     AdminRepository(self.redis)).find_by_id(1)
    # self.assertEqual(AdminModel.query.count(), 1)
    # self.assertIsInstance(find_admin_by_id, ServiceResult)
    # self.assertTrue(find_admin_by_id.success)
    # self.assert200(find_admin_by_id.data)
    # self.assertEqual(find_admin_by_id.exception_case, None)
    # def test_create_error(self):
    #     self.test_add_pin()
    #
    #     with self.client:
    #         response = self.client.post(
    #             "/api/v1/customers/accounts/", json=self.account_creation_data
    #         )
    #         self.assertStatus(response, 400)
    #
    # def test_create_route_error(self):
    #     with self.client:
    #         customer = self.client.post("/api/v1/customers/accounts/", json={})
    #         self.assertStatus(customer, 400)
    #
    # def test_update_route(self):
    #     customer = self.customer_repository.create(self.customer_data)
    #     self.assertEqual(customer.phone_number, self.customer_data["phone_number"])
    #     with self.client:
    #         customer_update = self.client.patch(
    #             f"/api/v1/customers/accounts/{customer.id}",
    #             json={"first_name": "Jane"},
    #             headers=self.headers,
    #         )
    #
    #         self.assert200(customer_update)
    #
    #     customer_search = self.customer_repository.find_by_id(customer.id)
    #     self.assertEqual(customer_search.first_name, "Jane")
    #
    # def test_delete_route(self):
    #     customer = self.customer_repository.create(self.customer_data)
    #     self.assertEqual(customer.phone_number, self.customer_data["phone_number"])
    #
    #     with self.client:
    #         response = self.client.delete(
    #             f"/api/v1/customers/accounts/{customer.id}", headers=self.headers
    #         )
    #         self.assertStatus(response, 204)
    #
    #     with self.assertRaises(AppException.NotFoundException):
    #         self.customer_repository.find_by_id(customer.id)
    #
    # def test_show_route(self):
    #     customer = self.customer_repository.create(self.customer_data)
    #     self.assertEqual(customer.phone_number, self.customer_data["phone_number"])
    #
    #     with self.client:
    #         response = self.client.get(
    #             f"/api/v1/customers/accounts/{customer.id}", headers=self.headers
    #         )
    #         self.assertStatus(response, 200)
    #         data = response.json
    #
    #         self.assertEqual(
    #             data.get("first_name"), self.customer_data.get("first_name")
    #         )
    #
    # def test_confirm_token_route(self):
    #     result = self.test_create_route()
    #     id = result.get("id")
    #     lead = self.lead_repository.find_by_id(id)
    #     token = lead.otp
    #
    #     with self.client:
    #         response = self.client.post(
    #             "/api/v1/customers/confirm-token", json={"id": id, "token": token}
    #         )
    #         self.assertStatus(response, 200)
    #
    #         return response.json
    #
    # def test_wrong_token(self):
    #     result = self.test_create_route()
    #     id = result.get("id")
    #
    #     with self.client:
    #         response = self.client.post(
    #             "/api/v1/customers/confirm-token", json={"id": id, "token": "11111"}
    #         )
    #         self.assertStatus(response, 400)
    #
    # def test_resend_token(self):
    #     result = self.test_create_route()
    #     id = result.get("id")
    #
    #     with self.client:
    #         response = self.client.post(
    #             "/api/v1/customers/resend-token", json={"id": id}
    #         )
    #
    #         self.assertStatus(response, 200)
    #
    # @mock.patch("app.services.keycloak_service.AuthService.create_user")
    # def test_add_pin(self, mock_create_user):
    #     mock_create_user.side_effect = self.auth_service.create_user
    #
    #     result = self.test_confirm_token_route()
    #     with self.client:
    #         response = self.client.post(
    #             "/api/v1/customers/add-pin",
    #             json={"password_token": result.get("password_token"), "pin": "1234"},
    #         )
    #         self.assertStatus(response, 201)
    #         data = response.json
    #         self.assertIn("access_token", data)
    #         self.assertIn("refresh_token", data)
    #
    # @mock.patch("app.services.keycloak_service.AuthService.get_token")
    # def test_login(self, mock_get_token):
    #     mock_get_token.side_effect = self.auth_service.get_token
    #     self.test_add_pin()
    #
    #     with self.client:
    #         response = self.client.post(
    #             "/api/v1/customers/token-login",
    #             json={"phone_number": "0242111111", "pin": "1234"},
    #         )
    #         self.assertStatus(response, 200)
    #         data = response.json
    #         self.assertIn("access_token", data)
    #         self.assertIn("refresh_token", data)
    #
    # @mock.patch("app.services.keycloak_service.AuthService.get_token")
    # @mock.patch("app.services.keycloak_service.AuthService.reset_password")
    # @mock.patch("core.utils.auth.jwt.decode")
    # def test_change_password(self, mock_jwt, mock_reset_password, mock_get_token):
    #     mock_reset_password.side_effect = self.auth_service.reset_password
    #     mock_get_token.side_effect = self.auth_service.get_token
    #
    #     self.test_add_pin()
    #
    #     customer = self.customer_repository.find_all({})[0]
    #
    #     self.required_roles["preferred_username"] = str(customer.id)
    #     mock_jwt.side_effect = self.required_roles_side_effect
    #
    #     with self.client:
    #         response = self.client.post(
    #             "/api/v1/customers/change-password",
    #             headers={"Authorization": f"Bearer {self.access_token}"},
    #             json={"old_pin": "1234", "new_pin": "0000"},
    #         )
    #         self.assert_status(response, 204)
    #
    # @mock.patch("app.services.keycloak_service.AuthService.reset_password")
    # def test_forgot_password(self, mock_reset_password):
    #     mock_reset_password.side_effect = self.auth_service.reset_password
    #     self.test_add_pin()
    #
    #     with self.client:
    #         response = self.client.post(
    #             "api/v1/customers/request-reset",
    #             json={"phone_number": self.customer_data.get("phone_number")},
    #         )
    #
    #         self.assert_200(response)
    #
    #         data = response.json
    #
    #         self.assertIn("id", data)
    #
    #         token_id = data.get("id")
    #
    #         # get token from the database
    #         token = self.customer_repository.find_by_id(token_id).auth_token
    #
    #         response = self.client.post(
    #             "api/v1/customers/reset-password",
    #             json={
    #                 "token": token,
    #                 "id": token_id,
    #                 "new_pin": "1116",
    #             },
    #         )
    #
    #         self.assertStatus(response, 204)
