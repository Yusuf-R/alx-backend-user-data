#!/usr/bin/env python3
""" Basic Auth template"""

from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """
    BasicAuth class provides basic authentication capabilities
    in a Flask application.

    Methods:
    - require_auth(path: str, excluded_paths: List[str]) -> bool:
        Determines whether authentication is required for a given path.
    - authorization_header(request=None) -> str:
        Retrieves the authorization header from a request.
    - current_user(request=None) -> TypeVar('User'): Returns None.

    Fields:
    - None.
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        Extracts the base64 authorization header from the given string.

        Args:
            authorization_header (str): The authorization header string.

        Returns:
            str: The extracted base64 authorization header.
        """
        # Check if the authorization header is None
        if authorization_header is None:
            return None

        # Check if the authorization header is of type string
        if not isinstance(authorization_header, str):
            return None

        # Check if the authorization header starts with 'Basic '
        if not authorization_header.startswith('Basic '):
            return None

        # Extract and return the base64 authorization header
        return authorization_header.split(' ')[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Decodes a base64 authorization header.

        Args:
            base64_authorization_header (str):
            The base64 authorization header to decode.

        Returns:
            str: The decoded authorization header,
                  or None if decoding fails.
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            return (base64.b64decode(base64_authorization_header)
                    .decode('utf-8'))
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Extracts user credentials from a decoded base64
        authorization header.

        Args:
            decoded_base64_authorization_header (str):
                The decoded base64 authorization header.

        Returns:
            tuple: A tuple containing the extracted user credentials.
                The first element is the username and the second element
                    is the password.
                If any of the conditions in the flow are not met,
                    `(None, None)` is returned.
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        data = decoded_base64_authorization_header.split(':', maxsplit=1)
        return (data[0], data[1])

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Retrieve a user object based on the provided email
        and password credentials.

        Args:
            user_email (str): The email address of the user.
            user_pwd (str): The password of the user.

        Returns:
            TypeVar('User'): The user object corresponding to the
                provided email and password credentials.
            Returns None if the credentials are invalid or
            if an exception occurs during the process.
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            obj = User.search({'email': user_email})
            if len(obj) == 0:
                return None
            for user_obj in obj:
                if user_obj.is_valid_password(user_pwd):
                    return user_obj
        except Exception:
            return None
