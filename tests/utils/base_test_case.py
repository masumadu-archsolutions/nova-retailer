import os
from flask_testing import TestCase
from app import create_app, db, APP_ROOT
from app.controllers import RetailerController
from app.repositories import RetailerRepository
from tests import MockAuthService
from config import Config
from unittest.mock import patch
import fakeredis

from app.models import RetailerModel

# from app.services import RedisService
from tests import (
    existing_retailer,
    retailer_credential,
    new_retailer,
    update_retailer,
)


class BaseTestCase(TestCase):
    required_roles = {"resource_access": {"nova_retailer": {"roles": ["retailer"]}}}

    def create_app(self):
        app = create_app("config.TestingConfig")

        # dummy access token
        self.access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"  # noqa: E501
        # dummy refresh token same as access token
        self.refresh_token = self.access_token

        self.headers = {"Authorization": f"Bearer {self.access_token}"}

        self.setup_patches()
        self.instantiate_classes(self.redis)
        return app

    def instantiate_classes(self, redis_server):
        self.retailer_repository = RetailerRepository(redis_service=redis_server)
        self.auth_service = MockAuthService()
        self.retailer_controller = RetailerController(
            retailer_repository=self.retailer_repository,
            auth_service=self.auth_service,
        )

    def setup_patches(self):
        redis_patcher = patch(
            "app.services.redis_service.redis_conn", fakeredis.FakeStrictRedis()
        )
        self.addCleanup(redis_patcher.stop)
        self.redis = redis_patcher.start()
        kafka_patcher = patch(
            "app.notifications.sms_notification_handler.publish_to_kafka",
            self.dummy_kafka_method,
        )
        self.addCleanup(kafka_patcher.stop)
        kafka_patcher.start()
        patcher = patch("core.utils.auth.jwt.decode", self.token_decode)
        self.addCleanup(patcher.stop)
        patcher.start()
        utc_patcher = patch(
            "app.controllers.retailer_controller.utc.localize", self.utc_side_effect
        )
        self.addCleanup(utc_patcher.stop)
        utc_patcher.start()

    def setUp(self):
        """
        Will be called before every test
        """
        db.create_all()
        self.existing_retailer = existing_retailer
        self.retailer_credentials = retailer_credential
        self.update_retailer = update_retailer
        self.create_retailer = new_retailer
        self.model_data = RetailerModel(**self.existing_retailer)
        db.session.add(self.model_data)
        db.session.commit()

    def tearDown(self):
        """
        Will be called after every test
        """
        db.session.remove()
        db.drop_all()

        file = f"{Config.SQL_DB_NAME}.sqlite3"
        file_path = os.path.join(APP_ROOT, file)
        os.remove(file_path)

    def dummy_kafka_method(self, topic, value):
        return True

    def token_decode(self, token, key, algorithms, audience, issuer):  # noqa
        return self.required_roles

    def utc_side_effect(self, args):  # noqa
        return args
