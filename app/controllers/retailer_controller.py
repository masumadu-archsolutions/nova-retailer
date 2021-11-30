import random
import secrets
import pytz
from datetime import datetime, timedelta

from core import Result
from core.exceptions import AppException
from core.notifier import Notifier
from core.service_interfaces import AuthServiceInterface
from app.repositories import RetailerRepository
from app.notifications import SMSNotificationHandler

utc = pytz.UTC

USER_DOES_NOT_EXIST = "user does not exist"


class RetailerController(Notifier):
    def __init__(
        self,
        retailer_repository: RetailerRepository,
        auth_service: AuthServiceInterface,
    ):
        self.retailer_repository = retailer_repository
        self.auth_service = auth_service

    def create_retailer(self, retailer_data):
        phone_number = retailer_data.get("phone_number")
        existing_retailer = self.retailer_repository.find({"phone_number": phone_number})

        if existing_retailer:
            raise AppException.ResourceExists(
                context=f"retailer with phone number {phone_number} exists"
            )
        retailer = self.retailer_repository.create(retailer_data)
        user_data = {
            "username": retailer.id,
            "first_name": retailer.first_name,
            "last_name": retailer.last_name,
            "password": retailer_data.get("pin"),
            "group": "retailer",
        }

        # Create user in auth service
        auth_result = self.auth_service.create_user(user_data)
        # return Result({"id": retailer.id}, 201)
        return Result({"id": auth_result}, 201)

    # def find_retailer(self, retailer_id):
    #     retailer = self.retailer_repository.find_by_id(retailer_id)
    #     return Result(retailer, 200)
    #
    # def update_retailer(self, retailer_id, retailer_data):
    #     retailer = self.retailer_repository.update_by_id(retailer_id, retailer_data)
    #     result = Result(retailer, 200)
    #     return result
    #
    # def login(self, retailer_credential):
    #     phone_number = retailer_credential.get("phone_number")
    #     pin = retailer_credential.get("pin")
    #     retailer = self.retailer_repository.find({"phone_number": phone_number})
    #     if not retailer:
    #         raise AppException.NotFoundException(
    #             context=f"retailer with phone number {phone_number} does not exists"
    #         )
    #
    #     access_token = self.auth_service.get_token(
    #         {"username": retailer.id, "password": pin}
    #     )
    #
    #     return Result(access_token, 200)
    #
    # def delete(self, retailer_id):
    #     self.retailer_repository.delete(retailer_id)
    #     result = Result({}, 204)
    #     return result
    #
    # def confirm_token(self, data):
    #     uuid = data.get("id")
    #     otp = data.get("token")
    #     lead = self.lead_repository.find({"id": uuid, "otp": otp})
    #     if not lead:
    #         raise AppException.BadRequest("Invalid authentication token")
    #
    #     assert lead.otp == otp, "Wrong token"
    #
    #     if utc.localize(datetime.now()) > lead.otp_expiration:
    #         raise AppException.ExpiredTokenException("the token you passed is expired")
    #
    #     password_token = secrets.token_urlsafe(16)
    #
    #     updated_lead = self.lead_repository.update_by_id(
    #         lead.id,
    #         {
    #             "password_token": password_token,
    #             "password_token_expiration": datetime.now() + timedelta(minutes=3),
    #         },
    #     )
    #
    #     token_data = {"password_token": updated_lead.password_token}
    #     return Result(token_data, 200)
    #
    # def resend_token(self, lead_id):
    #     lead = self.lead_repository.find_by_id(lead_id)
    #     auth_token = random.randint(100000, 999999)
    #     otp_expiration = datetime.now() + timedelta(minutes=5)
    #
    #     updated_lead = self.lead_repository.update_by_id(
    #         lead_id, {"otp": auth_token, "otp_expiration": otp_expiration}
    #     )
    #
    #     self.notify(
    #         SMSNotificationHandler(
    #             recipient=lead.phone_number,
    #             details={"verification_code": auth_token},
    #             meta={"type": "sms_notification", "subtype": "otp"},
    #         )
    #     )
    #     return Result({"id": updated_lead.id}, 200)
    #
    # def add_pin(self, data):
    #     token = data.get("password_token")
    #     pin = data.get("pin")
    #
    #     # find if password_token exists
    #     user = self.lead_repository.find({"password_token": token})
    #
    #     if not user:
    #         raise AppException.NotFoundException(USER_DOES_NOT_EXIST)
    #
    #     # Check if password_token is valid or expired
    #     if utc.localize(datetime.now()) > user.password_token_expiration:
    #         raise AppException.ExpiredTokenException("token expired")
    #
    #     user_data = {
    #         "username": str(user.id),
    #         "first_name": user.first_name,
    #         "last_name": user.last_name,
    #         "password": pin,
    #         "group": "retailer",
    #     }
    #     # Create user in auth service
    #     auth_result = self.auth_service.create_user(user_data)
    #
    #     # Create user in retailer table
    #     retailer_data = {
    #         "id": user.id,
    #         "phone_number": user.phone_number,
    #         "first_name": user.first_name,
    #         "last_name": user.last_name,
    #         "id_type": user.id_type,
    #         "id_number": user.id_number,
    #         "status": "active",
    #         "auth_service_id": auth_result.get("id"),
    #     }
    #
    #     self.retailer_repository.create(retailer_data)
    #     # Remove id from auth_result
    #     auth_result.pop("id", None)
    #     return Result(auth_result, 201)
    #
    # def change_password(self, data):
    #     retailer_id = data.get("retailer_id")
    #     new_pin = data.get("new_pin")
    #     old_pin = data.get("old_pin")
    #     retailer = self.retailer_repository.find_by_id(retailer_id)
    #     if not retailer:
    #         raise AppException.NotFoundException(USER_DOES_NOT_EXIST)
    #     self.auth_service.get_token({"username": str(retailer.id), "password": old_pin})
    #     self.auth_service.reset_password(
    #         {
    #             "user_id": str(retailer.auth_service_id),
    #             "new_password": new_pin,
    #         }
    #     )
    #     return Result({}, 204)
    #
    # def request_password_reset(self, data):
    #     phone_number = data.get("phone_number")
    #     retailer = self.retailer_repository.find({"phone_number": phone_number})
    #
    #     if not retailer:
    #         raise AppException.NotFoundException("User not found")
    #
    #     auth_token = random.randint(100000, 999999)
    #     auth_token_expiration = datetime.now() + timedelta(minutes=5)
    #     self.retailer_repository.update_by_id(
    #         retailer.id,
    #         {"auth_token": auth_token, "auth_token_expiration": auth_token_expiration},
    #     )
    #     self.notify(
    #         SMSNotificationHandler(
    #             recipient=retailer.phone_number,
    #             details={"verification_code": auth_token},
    #             meta={"type": "sms_notification", "subtype": "otp"},
    #         )
    #     )
    #     return Result({"id": retailer.id}, 200)
    #
    # def reset_password(self, data):
    #     auth_token = data.get("token")
    #     new_pin = data.get("new_pin")
    #     retailer_id = data.get("id")
    #
    #     retailer = self.retailer_repository.find_by_id(retailer_id)
    #     if not retailer:
    #         raise AppException.NotFoundException("User not found")
    #
    #     assert retailer.auth_token == auth_token, "Wrong token"
    #
    #     if utc.localize(datetime.now()) > retailer.auth_token_expiration:
    #         raise AppException.ExpiredTokenException("token expired")
    #
    #     self.auth_service.reset_password(
    #         {"user_id": str(retailer.auth_service_id), "new_password": new_pin}
    #     )
    #     self.notify(
    #         SMSNotificationHandler(
    #             recipient=retailer.phone_number,
    #             details={"name": retailer.first_name},
    #             meta={"type": "sms_notification", "subtype": "pin_change"},
    #         )
    #     )
    #
    #     return Result("", 204)
