#!/usr/bin/env python3
"""
Basic authentication module for the API
"""


from models.user import User
from typing import TypeVar
import base64
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """BasicAuth class"""
    def extract_base64_authorization_header(
            self, authorization_header: str
            ) -> str:
        """Returns the Base64 part of the Auth header for a Basic Auth"""
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None

        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str
            ) -> str:
        """Returns the decoded value of a Base64 string"""
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            decoded_string = decoded_bytes.decode('utf-8')
            return decoded_string
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str
            ) -> (str, str):
        """Returns the user email and password from the Base64 decoded value"""
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)

        return tuple(decoded_base64_authorization_header.split(':', 1))

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str
            ) -> TypeVar('User'):
        """Returns the User instance based on his email and password"""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            """search for users with matching email"""
            users = User.search({'email': user_email})
            """if no user is found with that email"""
        except Exception:
            return None

        if not users:
            return None

        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None

        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """Overloads Auth and retrieves the User instance for a request"""
        if request is None:
            return None

        """get authorization header"""
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None

        """extract base64 part of the header"""
        b64_auth_token = self.extract_base64_authorization_header(request)
        if b64_auth_token is None:
            return None

        """decode the base64 part"""
        decoded_token = self.decode_base64_authorization_header(b64_auth_token)
        if decoded_token is None:
            return None

        """extract user credentials"""
        email, password = self.extract_user_credentials(decoded_token)
        if email is None or password is None:
            return None

        """get user instance"""
        user = self.user_object_from_credentials(email, password)
        return user
