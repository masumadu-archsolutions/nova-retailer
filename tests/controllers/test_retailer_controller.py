import uuid
from core import Result
from core.exceptions import AppException
from app.utils import IDEnum
from tests.utils.base_test_case import BaseTestCase
from app.models import Retailer
import pytest


class TestRetailerController(BaseTestCase):

    # retailer_data = {
    #     "phone_number": "0244444444",
    #     "first_name": "John",
    #     "last_name": "Doe",
    #     "id_type": "passport",
    #     "id_number": "4829h9445839",
    #     "pin": "1234",
    # }

    @pytest.mark.retailer_controller
    def test_create_customer(self):
        retailer = self.retailer_controller.create_retailer(self.test_data)
        self.assertEqual(Retailer.query.count(), 1)
        self.assertIsInstance(retailer, Result)
        self.assertIn("id", retailer.value)
        self.assertEqual(retailer.status_code, 201)
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
