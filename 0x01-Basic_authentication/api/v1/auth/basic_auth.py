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

    pass
