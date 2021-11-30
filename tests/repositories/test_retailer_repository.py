# import uuid
# from core.exceptions import AppException
from app.utils import IDEnum
from tests.utils.base_test_case import BaseTestCase
import pytest
from app.models import Retailer


class TestRetailerRepository(BaseTestCase):
    # auth_service_id = str(uuid.uuid4())

    # retailer_data = {
    #     "phone_number": "0244444444",
    #     "first_name": "John",
    #     "last_name": "Doe",
    #     "id_type": "passport",
    #     "id_number": "4829h9445839",
    #     "pin": "1234"
    #     # "auth_service_id": auth_service_id,
    # }

    @pytest.mark.retailer_repository
    def test_create(self):
        retailer = self.retailer_repository.create(self.retailer_data)
        self.assertEqual(Retailer.query.count(), 1)
        self.assertIsInstance(retailer, Retailer)
        self.assertIsNotNone(retailer.id)
        self.assertEqual(self.retailer_data["first_name"], retailer.first_name)
        self.assertEqual(self.retailer_data["last_name"], retailer.last_name)
        self.assertEqual(self.retailer_data["phone_number"], retailer.phone_number)
        self.assertEqual(IDEnum.passport, retailer.id_type)
        self.assertEqual(self.retailer_data["id_number"], retailer.id_number)
        self.assertTrue(retailer.verify_password(self.retailer_data.get("pin")))
        # self.assertEqual(NEW_ADMIN_DATA["email"], create_new_admin.email)
        # self.assertEqual(NEW_ADMIN_DATA["username"], create_new_admin.username)
        # self.assertTrue(
        #     create_new_admin.verify_password(NEW_ADMIN_DATA["password"]))
        # self.assertEqual(customer.first_name, "John")

    # def test_update(self):
    #     customer = self.customer_repository.create(self.customer_data)
    #
    #     self.assertEqual(customer.first_name, "John")
    #
    #     updated_customer = self.customer_repository.update_by_id(
    #         customer.id, {"first_name": "Joe"}
    #     )
    #
    #     self.assertEqual(updated_customer.first_name, "Joe")
    #
    # def test_delete(self):
    #     customer = self.customer_repository.create(self.customer_data)
    #     customer_search = self.customer_repository.find_by_id(customer.id)
    #
    #     self.assertEqual(customer_search.id, customer.id)
    #     self.assertEqual(customer_search.id_type, IDEnum.passport)
    #
    #     self.customer_repository.delete(customer.id)
    #
    #     with self.assertRaises(AppException.NotFoundException):
    #         self.customer_repository.find_by_id(customer.id)
    #
    # def test_required_fields(self):
    #     customer_data = {
    #         "last_name": "Doe",
    #         "id_type": "passport",
    #         "id_number": "4829h9445839",
    #     }
    #
    #     with self.assertRaises(AppException.OperationError):
    #         self.customer_repository.create(customer_data)
    #
    # def test_duplicates(self):
    #     self.customer_repository.create(self.customer_data)
    #
    #     with self.assertRaises(AppException.OperationError):
    #         self.customer_repository.create(self.customer_data)
