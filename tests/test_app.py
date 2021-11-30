import os
from tests.utils.base_test_case import BaseTestCase
import pytest


class TestAppConfig(BaseTestCase):
    @pytest.mark.app
    def test_app_config(self):
        self.assertTrue(self.create_app().config["DEBUG"])
        self.assertTrue(self.create_app().config["TESTING"])
        self.assertTrue(self.create_app().config["DEVELOPMENT"])
        self.assertEqual(self.create_app().config["SECRET_KEY"], os.getenv("SECRET_KEY"))
