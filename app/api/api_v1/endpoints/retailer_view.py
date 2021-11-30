import pinject
from flask import Blueprint, request
from app.services import RedisService

from app.controllers import RetailerController
from core.service_result import handle_result
from app.repositories import RetailerRepository
from app.schema import (
    RetailerCreateSchema, RetailerSchema, LoginSchema,
    TokenSchema, RetailerReadSchema, RetailerUpdateSchema,
    # RetailerUpdateSchema,
    # ConfirmTokenSchema, AddPinSchema, ResendTokenSchema,
    # LoginSchema, TokenSchema, PinChangeSchema,
    # PinResetSchema, PinResetRequestSchema,
)
from app.services import AuthService
from core.utils import validator, auth_required

retailer = Blueprint("retailer", __name__)

obj_graph = pinject.new_object_graph(
    modules=None,
    classes=[
        RetailerController,
        RedisService,
        RetailerRepository,
        AuthService,
    ],
)
retailer_controller = obj_graph.provide(RetailerController)


@retailer.route("accounts/register", methods=["POST"])
@validator(schema=RetailerCreateSchema)
def create_retailer():
    """
    ---
    post:
      description: creates a new retailer
      requestBody:
        required: true
        content:
          application/json:
            schema: RetailerCreate
      responses:
        '201':
          description: returns a retailer id
          content:
            application/json:
              schema:
                type: object
                properties:
                  id:
                    type: uuid
                    example: 3fa85f64-5717-4562-b3fc-2c963f66afa6
      tags:
          - Authentication
    """
    retailer_data = request.json
    result = retailer_controller.create_retailer(retailer_data)
    return handle_result(result, schema=RetailerSchema)


# @retailer.route("/accounts/<string:retailer_id>", methods=["GET"])
# @auth_required()
# def find_retailer(retailer_id):
#     """
#     ---
#     get:
#       description: returns a retailer with id specified in path
#       parameters:
#         - in: path
#           name: retailer_id
#           required: true
#           schema:
#             type: string
#           description: The retailer ID
#       security:
#         - bearerAuth: []
#       responses:
#         '200':
#           description: returns a retailer
#           content:
#             application/json:
#               schema: Retailer
#       tags:
#           - Retailer
#     """
#     result = retailer_controller.find_retailer(retailer_id)
#     return handle_result(result, schema=RetailerReadSchema)


# @retailer.route("/accounts/<string:retailer_id>", methods=["PATCH"])
# @validator(schema=RetailerUpdateSchema)
# @auth_required()
# def update_retailer(retailer_id):
#     """
#     ---
#     patch:
#       description: updates a retailer with id specified in path
#       parameters:
#         - in: path
#           name: retailer_id
#           required: true
#           schema:
#             type: string
#           description: The retailer ID
#       requestBody:
#         required: true
#         content:
#             application/json:
#                 schema: retailerUpdate
#       security:
#         - bearerAuth: []
#       responses:
#         '200':
#           description: returns a retailer
#           content:
#             application/json:
#               schema: Retailer
#       tags:
#           - Retailer
#     """
#
#     retailer_data = request.json
#     result = retailer_controller.update_retailer(retailer_id, retailer_data)
#     return handle_result(result, schema=RetailerReadSchema)


# @retailer.route("/accounts/login", methods=["POST"])
# @validator(schema=LoginSchema)
# def login_retailer():
#     """
#     ---
#     post:
#       description: logs in a retailer
#       requestBody:
#         required: true
#         content:
#             application/json:
#                 schema: LoginSchema
#       responses:
#         '200':
#           description: call successful
#           content:
#             application/json:
#               schema: TokenData
#       tags:
#           - Authentication
#     """
#     retailer_credentials = request.json
#     result = retailer_controller.login(retailer_credentials)
#     return handle_result(result, schema=TokenSchema)
#

# @retailer.route("/confirm-token", methods=["POST"])
# @validator(schema=ConfirmTokenSchema)
# def confirm_token():
#     """
#     ---
#     post:
#       description: creates a new retailer
#       requestBody:
#         required: true
#         content:
#             application/json:
#                 schema: ConfirmToken
#       responses:
#         '200':
#           description: returns a retailer
#           content:
#             application/json:
#               schema:
#                 type: object
#                 properties:
#                   id:
#                     type: string
#                     example: m8bQ5_P8o_4eojNs4xUB6w
#       tags:
#           - Authentication
#     """
#
#     data = request.json
#     result = retailer_controller.confirm_token(data)
#     return handle_result(result)
#
#
# @retailer.route("/resend-token", methods=["POST"])
# @validator(schema=ResendTokenSchema)
# def resend_token():
#     """
#     ---
#     post:
#       description: creates a new token
#       requestBody:
#         required: true
#         content:
#           application/json:
#             schema: ResendTokenData
#       responses:
#         '200':
#           description: resends a token
#           content:
#             application/json:
#               schema:
#                 type: object
#                 properties:
#                   id:
#                     type: uuid
#                     example: 3fa85f64-5717-4562-b3fc-2c963f66afa6
#       tags:
#           - Authentication
#     """
#
#     data = request.json
#     result = retailer_controller.resend_token(data)
#     return handle_result(result)
#
#
# @retailer.route("/add-pin", methods=["POST"])
# @validator(schema=AddPinSchema)
# def add_pin():
#     """
#     ---
#     post:
#       description: creates a new retailer
#       requestBody:
#         required: true
#         content:
#             application/json:
#                 schema: PinData
#       responses:
#         '200':
#           description: returns a retailer
#           content:
#             application/json:
#               schema: TokenData
#       tags:
#           - Authentication
#     """
#
#     data = request.json
#     result = retailer_controller.add_pin(data)
#     return handle_result(result, schema=TokenSchema)
#
#

#
# @retailer.route("/accounts/<string:retailer_id>", methods=["PATCH"])
# @validator(schema=RetailerUpdateSchema)
# @auth_required()
# def update_retailer(retailer_id):
#     """
#     ---
#     patch:
#       description: updates a retailer with id specified in path
#       parameters:
#         - in: path
#           name: retailer_id
#           required: true
#           schema:
#             type: string
#           description: The retailer ID
#       requestBody:
#         required: true
#         content:
#             application/json:
#                 schema: retailerUpdate
#       security:
#         - bearerAuth: []
#       responses:
#         '200':
#           description: returns a retailer
#           content:
#             application/json:
#               schema: retailer
#       tags:
#           - retailer
#     """
#
#     data = request.json
#     result = retailer_controller.update(retailer_id, data)
#     return handle_result(result, schema=RetailerSchema)
#
#
# @retailer.route("/accounts/<string:retailer_id>", methods=["GET"])
# @auth_required()
# def show_retailer(retailer_id):
#     """
#     ---
#     get:
#       description: returns a retailer with id specified in path
#       parameters:
#         - in: path
#           name: retailer_id
#           required: true
#           schema:
#             type: string
#           description: The retailer ID
#       security:
#         - bearerAuth: []
#       responses:
#         '200':
#           description: returns a retailer
#           content:
#             application/json:
#               schema: retailer
#       tags:
#           - retailer
#     """
#     result = retailer_controller.show(retailer_id)
#     return handle_result(result, schema=RetailerSchema)
#
#
# @retailer.route("/accounts/<string:retailer_id>", methods=["DELETE"])
# @auth_required()
# def delete_retailer(retailer_id):
#     """
#     ---
#     delete:
#       description: deletes a retailer with id specified in path
#       parameters:
#         - in: path
#           name: retailer_id
#           required: true
#           schema:
#             type: string
#           description: The retailer ID
#       security:
#         - bearerAuth: []
#       responses:
#         '204':
#           description: returns nil
#       tags:
#           - retailer
#     """
#     result = retailer_controller.delete(retailer_id)
#     return handle_result(result)
#
#
# @retailer.route("/change-password", methods=["POST"])
# @validator(schema=PinChangeSchema)
# @auth_required()
# def change_password(user_id):
#     """
#     ---
#     post:
#       description: changes a retailer's password
#       requestBody:
#         required: true
#         content:
#             application/json:
#                 schema: PinChange
#       security:
#         - bearerAuth: []
#       responses:
#         '204':
#           description: returns nil
#       tags:
#           - Authentication
#     """
#     data = request.json
#     data["retailer_id"] = user_id
#     result = retailer_controller.change_password(data)
#     return handle_result(result)
#
#
# @retailer.route("/request-reset", methods=["POST"])
# @validator(schema=PinResetRequestSchema)
# def forgot_password():
#     """
#     ---
#     post:
#       description: requests a reset of a retailer's password
#       requestBody:
#         required: true
#         content:
#             application/json:
#                 schema: PinResetRequest
#       responses:
#         '200':
#           description: returns a uuid (retailer's id)
#           content:
#             application/json:
#               schema:
#                 type: object
#                 properties:
#                   id:
#                     type: uuid
#                     example: 3fa85f64-5717-4562-b3fc-2c963f66afa6
#       tags:
#           - Authentication
#     """
#     data = request.json
#     result = retailer_controller.request_password_reset(data)
#     return handle_result(result)
#
#
# @retailer.route("/reset-password", methods=["POST"])
# @validator(schema=PinResetSchema)
# def reset_password():
#     """
#     ---
#     post:
#       description: confirms reset of a retailer's password
#       requestBody:
#         required: true
#         content:
#             application/json:
#                 schema: PinReset
#       responses:
#         '204':
#           description: returns nil
#       tags:
#           - Authentication
#     """
#     data = request.json
#     result = retailer_controller.reset_password(data)
#     return handle_result(result)
