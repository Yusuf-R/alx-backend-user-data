#!/usr/bin/env python3
""" Base template for the auth functionality"""

from flask import request
from typing import List, TypeVar
from os import getenv


class Auth():
    """ Base class for the auth
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ require_auth """
        return False

    def authorization_header(self, request=None) -> str:
        """ authorization_header """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ current_user """
        return None
