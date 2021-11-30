"""
Constants.py
Contains all string constants used in this service
"""
KEYCLOAK_UNAVAILABLE = "keycloak server unavailable"
KEYCLOAK_POST = "keycloak_post_error"
KEYCLOAK_PUT = "keycloak_put_error"
KEYCLOAK_ADMIN_TOKEN = "keycloak_access_token_error"
KEYCLOAK_ACCESS_TOKEN = "keycloak_token_error"
KEYCLOAK_GROUP = "keycloak_group_error"
KEYCLOAK_REFRESH_TOKEN = "keycloak_refresh_token_error"
KEYCLOAK_USER = "keycloak_user_error"
USER_EXISTS = "user_exists"
NOT_FOUND = "not_found"
INVALID_TOKEN = "invalid_token"
KEYCLOAK_ERROR = "keycloak_error"
PHONE_NUMBER_REGEX = r"(\+?( |-|\.)?\d{1,2}( |-|\.)?)?(\(?\d{3}\)?|\d{3})( |-|\.)?(\d{3}( |-|\.)?\d{4})"  # noqa

# http request error definitions
KEYCLOAK_CONNECTION_ERROR = "keycloak server connection error"
KEYCLOAK_HTTP_ERROR = "keycloak server http error"
KEYCLOAK_CONNECTION_TIMEOUT = "keycloak server connection timedout"
KEYCLOAK_REQUEST_ERROR = "error connecting to keycloak server"
