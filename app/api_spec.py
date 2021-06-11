"""OpenAPI v3 Specification"""

# apispec via OpenAPI
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin

# Create an APISpec

spec = APISpec(
    title="Boilerplate project",
    version="1.0.0",
    openapi_version="3.0.2",
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)

# register schemas with spec
# example
# spec.components.schema("UserCreate", schema=UserCreate)


# add swagger tags that are used for endpoint annotation
tags = [
    {"name": "Authentication", "description": "For user authentication."},
]

for tag in tags:
    print(f"Adding tag: {tag['name']}")
    spec.tag(tag)
