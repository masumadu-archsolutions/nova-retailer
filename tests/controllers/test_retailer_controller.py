import unittest
from core import Result

# from core.exceptions import AppException
# from app.utils import IDEnum
from tests.utils.base_test_case import BaseTestCase
from app.models import RetailerModel
import pytest


class TestRetailerController(BaseTestCase):
    @pytest.mark.retailer_controller
    def test_create_retailer(self):
        retailer = self.retailer_controller.create_retailer(self.create_retailer)
        self.assertEqual(RetailerModel.query.count(), 2)
        self.assertIsInstance(retailer, Result)
        self.assertIn("id", retailer.value)
        self.assertEqual(retailer.status_code, 201)

    @pytest.mark.retailer_controller
    def test_login_retailer(self):
        retailer = self.retailer_controller.login(self.retailer_credentials)
        self.assertEqual(RetailerModel.query.count(), 1)
        self.assertIsInstance(retailer, Result)
        self.assertIsInstance(retailer.value, dict)
        self.assertEqual(len(retailer.value), 2)
        self.assertIn("access_token", retailer.value)
        self.assertIn("refresh_token", retailer.value)
        self.assertEqual(retailer.status_code, 200)

    @pytest.mark.retailer_controller
    def test_find_retailer(self):
        self.assertEqual(RetailerModel.query.count(), 1)
        retailer = RetailerModel.query.filter_by(
            phone_number=self.existing_retailer.get("phone_number")
        ).first()
        self.assertIsNotNone(retailer)
        self.assertIsNotNone(retailer.id)
        find_retailer = self.retailer_controller.find_retailer(retailer.id)
        self.assert200(find_retailer)
        self.assertIsNotNone(find_retailer)
        self.assertIsInstance(find_retailer, Result)
        self.assertIsInstance(find_retailer.value, RetailerModel)
        self.assertEqual(find_retailer.value, retailer)

    @pytest.mark.retailer_controller
    def test_update_retailer(self):
        self.assertEqual(RetailerModel.query.count(), 1)
        retailer = RetailerModel.query.filter_by(
            phone_number=self.existing_retailer.get("phone_number")
        ).first()
        self.assertIsNotNone(retailer)
        self.assertIsNotNone(retailer.id)
        update_retailer = self.retailer_controller.update_retailer(
            retailer.id, self.update_retailer
        )
        self.assert200(update_retailer)
        self.assertIsNotNone(update_retailer)
        self.assertIsInstance(update_retailer, Result)
        self.assertIsInstance(update_retailer.value, RetailerModel)
        self.assertEqual(retailer.id, update_retailer.value.id)
        self.assertEqual(
            update_retailer.value.phone_number, self.update_retailer.get("phone_number")
        )


if __name__ == "__main__":
    unittest.main()
    # self.assertIsInstance()
    # self.assertEqual(retailer.id, find_retailer.id)
    # self.assertTrue(create_new_admin.success)
    # self.assertEqual(create_new_admin.data.status_code, 201)
    # self.assertEqual(create_new_admin.exception_case, None)
    # updated_customer = self.customer_controller.update(
    #     customer.id,
    #     {
    #         "first_name": "Jane",
    #         "last_name": "Dew",
    #     },
    # )
    #
    # updated_data = updated_customer.value
    #
    # self.assertEqual(updated_data.id, customer.id)
    # self.assertEqual(updated_data.last_name, "Dew")
    # self.assertEqual(updated_data.first_name, "Jane")
    #
    # customer_search = self.customer_repository.find_by_id(updated_data.id)
    #
    # self.assertEqual(customer_search.id, updated_data.id)
    # self.assertEqual(customer_search.last_name, "Dew")

    # def test_edit_customer(self):
    #     customer = self.customer_repository.create(self.customer_data)
    #
    #     updated_customer = self.customer_controller.update(
    #         customer.id,
    #         {
    #             "first_name": "Jane",
    #             "last_name": "Dew",
    #         },
    #     )
    #
    #     updated_data = updated_customer.value
    #
    #     self.assertEqual(updated_data.id, customer.id)
    #     self.assertEqual(updated_data.last_name, "Dew")
    #     self.assertEqual(updated_data.first_name, "Jane")
    #
    #     customer_search = self.customer_repository.find_by_id(updated_data.id)
    #
    #     self.assertEqual(customer_search.id, updated_data.id)
    #     self.assertEqual(customer_search.last_name, "Dew")
    #
    # def test_delete_customer(self):
    #     customer = self.customer_repository.create(self.customer_data)
    #
    #     self.customer_controller.delete(customer.id)
    #
    #     with self.assertRaises(AppException.NotFoundException):
    #         self.customer_repository.find_by_id(customer.id)
    #
    # def test_show_customer(self):
    #     customer = self.customer_repository.create(self.customer_data)
    #     customer_search = self.customer_controller.show(customer.id)
    #
    #     customer_values = customer_search.value
    #     self.assertEqual(customer_values.id, customer.id)
    #     self.assertEqual(customer_values.last_name, "Doe")
    #     self.assertEqual(customer_values.id_type, IDEnum.passport)
