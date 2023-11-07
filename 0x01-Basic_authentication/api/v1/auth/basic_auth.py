#!/usr/bin/env python3
""" Basic Auth template"""

from api.v1.auth.auth import Auth
from flask import request
from typing import List
from os import getenv
import re


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
