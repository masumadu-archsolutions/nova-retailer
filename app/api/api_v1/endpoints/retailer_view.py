import pinject
from flask import Blueprint, request
from app.services import RedisService

from app.controllers import RetailerController
from core.service_result import handle_result
from app.repositories import RetailerRepository
from app.schema import (
    RetailerCreateSchema,
    RetailerSchema,
    LoginSchema,
    TokenSchema,
    RetailerUpdateSchema,
    # TokenSchema, RetailerReadSchema, RetailerUpdateSchema,
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
    data = request.json
    result = retailer_controller.create_retailer(data)
    return handle_result(result, schema=RetailerSchema)


@retailer.route("/accounts/login", methods=["POST"])
@validator(schema=LoginSchema)
def login_retailer():
    """
    ---
    post:
      description: logs in a retailer
      requestBody:
        required: true
        content:
            application/json:
                schema: LoginSchema
      responses:
        '200':
          description: call successful
          content:
            application/json:
              schema: TokenData
      tags:
          - Authentication
    """
    data = request.json
    result = retailer_controller.login(data)
    return handle_result(result, schema=TokenSchema)


@retailer.route("/accounts/<string:retailer_id>", methods=["GET"])
@auth_required()
def find_retailer(retailer_id):
    """
    ---
    get:
      description: returns a retailer with id specified in path
      parameters:
        - in: path
          name: retailer_id
          required: true
          schema:
            type: string
          description: The retailer ID
      security:
        - bearerAuth: []
      responses:
        '200':
          description: returns a retailer
          content:
            application/json:
              schema: Retailer
      tags:
          - Retailer
    """
    data = retailer_controller.find_retailer(retailer_id)
    return handle_result(data, schema=RetailerSchema)


@retailer.route("/accounts/<string:retailer_id>", methods=["PATCH"])
@validator(schema=RetailerUpdateSchema)
@auth_required()
def update_retailer(retailer_id):
    """
    ---
    patch:
      description: updates a retailer with id specified in path
      parameters:
        - in: path
          name: retailer_id
          required: true
          schema:
            type: string
          description: The Retailer ID
      requestBody:
        required: true
        content:
            application/json:
                schema: RetailerUpdate
      security:
        - bearerAuth: []
      responses:
        '200':
          description: returns a retailer
          content:
            application/json:
              schema: Retailer
      tags:
          - Retailer
    """

    data = request.json
    result = retailer_controller.update_retailer(retailer_id, data)
    return handle_result(result, schema=RetailerSchema)
