"""OpenAPI v3 Specification"""

# apispec via OpenAPI
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin

# Create an APISpec
from app.schema import (
    RetailerSchema,
    LoginSchema,
    RetailerCreateSchema,
    TokenSchema,
    RetailerUpdateSchema,
    # ConfirmTokenSchema,
    # AddPinSchema,
    # ResendTokenSchema,
    # LoginSchema,
    # PinChangeSchema,
    # PinResetSchema,
    # PinResetRequestSchema,
)

spec = APISpec(
    title="Nova Retailer Service",
    version="1.0.0",
    openapi_version="3.0.2",
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)

# Security
api_key_scheme = {"type": "apiKey", "in": "header", "name": "X-API-Key"}
bearer_scheme = {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
spec.components.security_scheme("ApiKeyAuth", api_key_scheme)
spec.components.security_scheme("bearerAuth", bearer_scheme)

# register schemas with spec
spec.components.schema("Retailer", schema=RetailerSchema)
spec.components.schema("RetailerCreate", schema=RetailerCreateSchema)
spec.components.schema("RetailerLogin", schema=LoginSchema)
spec.components.schema("TokenData", schema=TokenSchema)
spec.components.schema("RetailerUpdate", schema=RetailerUpdateSchema)
# spec.components.schema("ConfirmToken", schema=ConfirmTokenSchema)
# spec.components.schema("PinData", schema=AddPinSchema)
# spec.components.schema("ResendTokenData", schema=ResendTokenSchema)
# spec.components.schema("LoginData", schema=LoginSchema)
# spec.components.schema("TokenData", schema=TokenSchema)
# spec.components.schema("PinChange", schema=PinChangeSchema)
# spec.components.schema("PinReset", schema=PinResetSchema)
# spec.components.schema("PinResetRequest", schema=PinResetRequestSchema)


# add swagger tags that are used for endpoint annotation
tags = [
    {"name": "Authentication", "description": "For retailer authentication."},
    {"name": "Retailer", "description": "Retailer crud operation"},
]

for tag in tags:
    print(f"Adding tag: {tag['name']}")
    spec.tag(tag)
