from tests.utils.base_test_case import BaseTestCase
from app.models import RetailerModel
import unittest
import pytest


class TestModels(BaseTestCase):
    @pytest.mark.model
    def test_retailer_model(self):
        self.assertEqual(RetailerModel.query.count(), 1)
        retailer = RetailerModel.query.filter_by(
            phone_number=self.existing_retailer.get("phone_number")
        ).first()
        self.assertIsNotNone(retailer.id)
        self.assertEqual(self.model_data.id, retailer.id)
        self.assertEqual(retailer, self.model_data)


if __name__ == "__main__":
    unittest.main()
