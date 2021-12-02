# import uuid
# from core.exceptions import AppException
from app.utils import IDEnum
from tests.utils.base_test_case import BaseTestCase
import pytest
from app.models import RetailerModel
import unittest


class TestRetailerRepository(BaseTestCase):
    @pytest.mark.retailer_repository
    def test_create(self):
        retailer = self.retailer_repository.create(self.create_retailer)
        self.assertEqual(RetailerModel.query.count(), 2)
        self.assertIsInstance(retailer, RetailerModel)
        self.assertIsNotNone(retailer.id)
        self.assertEqual(self.create_retailer["first_name"], retailer.first_name)
        self.assertEqual(self.create_retailer["last_name"], retailer.last_name)
        self.assertEqual(self.create_retailer["phone_number"], retailer.phone_number)
        self.assertEqual(IDEnum.passport, retailer.id_type)
        self.assertEqual(self.create_retailer["id_number"], retailer.id_number)
        self.assertTrue(retailer.verify_password(self.create_retailer.get("pin")))

    @pytest.mark.retailer_repository
    def test_find_by_id(self):
        self.assertEqual(RetailerModel.query.count(), 1)
        retailer = RetailerModel.query.filter_by(
            phone_number=self.existing_retailer.get("phone_number")
        ).first()
        self.assertIsNotNone(retailer)
        self.assertIsInstance(retailer, RetailerModel)
        self.assertIsNotNone(retailer.id)
        self.assertEqual(retailer.first_name, self.existing_retailer.get("first_name"))
        find_retailer = self.retailer_repository.find_by_id(retailer.id)
        self.assertIsNotNone(find_retailer)
        self.assertIsInstance(retailer, RetailerModel)
        self.assertEqual(retailer.id, find_retailer.id)
        self.assertEqual(retailer.first_name, find_retailer.first_name)

    @pytest.mark.retailer_repository
    def test_update_by_id(self):
        self.assertEqual(RetailerModel.query.count(), 1)
        retailer = RetailerModel.query.filter_by(
            phone_number=self.existing_retailer.get("phone_number")
        ).first()
        self.assertIsNotNone(retailer)
        self.assertIsInstance(retailer, RetailerModel)
        self.assertIsNotNone(retailer.id)
        update_retailer = self.retailer_repository.update_by_id(
            retailer.id, self.update_retailer
        )
        self.assertIsNotNone(update_retailer)
        self.assertIsInstance(update_retailer, RetailerModel)
        self.assertEqual(retailer.id, update_retailer.id)
        self.assertEqual(
            update_retailer.phone_number, self.update_retailer.get("phone_number")
        )
        # # self.assertEqual(retailer.first_name,
        #                  self.existing_retailer.get("first_name"))
        # find_retailer = self.retailer_repository.find_by_id(retailer.id)
        # self.assertIsNotNone(find_retailer)
        # self.assertIsInstance(retailer, RetailerModel)
        # self.assertEqual(retailer.id, find_retailer.id)
        # self.assertEqual(retailer.first_name, find_retailer.first_name)


if __name__ == "__main__":
    unittest.main()

    # find_retailer.first_name)
    # self.assertEqual(self.create_retailer["last_name"],
    #                  retailer.last_name)
    # self.assertEqual(self.create_retailer["phone_number"],
    #                  retailer.phone_number)
    # self.assertEqual(IDEnum.passport, retailer.id_type)
    # self.assertEqual(self.create_retailer["id_number"],
    #                  retailer.id_number)
    # self.assertTrue(
    #     retailer.verify_password(self.create_retailer.get("pin")))
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
