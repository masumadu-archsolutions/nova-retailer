import uuid
from app.core.exceptions import AppException
from app.core.utils import IDEnum
from tests.utils.base_test_case import BaseTestCase


class TestCustomerRepository(BaseTestCase):
    auth_service_id = str(uuid.uuid4())

    customer_data = {
        "phone_number": "00233242583061",
        "first_name": "John",
        "last_name": "Doe",
        "id_type": "passport",
        "id_number": "4829h9445839",
        "auth_service_id": auth_service_id,
    }

    def test_create(self):
        customer = self.customer_repository.create(self.customer_data)
        self.assertEqual(customer.first_name, "John")

    def test_update(self):
        customer = self.customer_repository.create(self.customer_data)

        self.assertEqual(customer.first_name, "John")

        updated_customer = self.customer_repository.update_by_id(
            customer.id, {"first_name": "Joe"}
        )

        self.assertEqual(updated_customer.first_name, "Joe")

    def test_delete(self):
        customer = self.customer_repository.create(self.customer_data)
        customer_search = self.customer_repository.find_by_id(customer.id)

        self.assertEqual(customer_search.id, customer.id)
        self.assertEqual(customer_search.id_type, IDEnum.passport)

        self.customer_repository.delete(customer.id)

        with self.assertRaises(AppException.NotFoundException):
            self.customer_repository.find_by_id(customer.id)

    def test_required_fields(self):
        customer_data = {
            "last_name": "Doe",
            "id_type": "passport",
            "id_number": "4829h9445839",
        }

        with self.assertRaises(AppException.OperationError):
            self.customer_repository.create(customer_data)

    def test_duplicates(self):
        self.customer_repository.create(self.customer_data)

        with self.assertRaises(AppException.OperationError):
            self.customer_repository.create(self.customer_data)
