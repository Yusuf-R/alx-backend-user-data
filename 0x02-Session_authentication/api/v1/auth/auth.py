#!/usr/bin/env python3
""" Base template for the auth functionality"""

from flask import request
from typing import List, TypeVar
from os import getenv
import re


class Auth():
    """Base class for authentication in a Flask application.

    This class provides methods to determine whether authentication is required
    for a given path and to retrieve the authorization header from a request.

    Example Usage:
    ```python
    auth = Auth()
    path = "/api/users"
    excluded_paths = ["/api/login", "/api/register"]
    requires_auth = auth.require_auth(path, excluded_paths)
    print(requires_auth)  # True

    header = auth.authorization_header(request)
    print(header)  # None
    ```

    Methods:
    - require_auth(path: str, excluded_paths: List[str]) -> bool:
        Determines whether authentication is required for a given path.
    - authorization_header(request=None) -> str:
        Retrieves the authorization header from a request.

    Fields:
    - None
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Determine whether authentication is required for a given path.

        Args:
            path (str): The path for which authentication requirement
                needs to be determined.
            excluded_paths (List[str]): The list of paths that are excluded
                from authentication requirement.

        Returns:
            bool: True if authentication is required for the given path,
                False otherwise.
        """
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        for excluded_path in map(lambda x: x.strip(), excluded_paths):
            pattern = ''
            if excluded_path[-1] == '*':
                pattern = '{}.*'.format(excluded_path[:-1])
            elif excluded_path[-1] == '/':
                pattern = '{}/*'.format(excluded_path[:-1])
            else:
                pattern = '{}/*'.format(excluded_path)
            if re.match(pattern, path):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Retrieves the authorization header from a request.

        Args:
            request (optional): The request object from which to retrieve
            the authorization header.

        Returns:
            str: The authorization header as a string.
            If no request object is provided, returns None.
        """

        if request is None or request.headers.get('Authorization') is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ current_user """
        return None

    def session_cookie(self, request=None):
        """
        Retrieve the session cookie from a request object.

        Args:
            request (optional): The request object from which to
            retrieve the session cookie.

        Returns:
            str: the value of the session cookie
            None if the session cookie does not exist.
        """
        if request is None:
            return None
        session_name = getenv('SESSION_NAME')
        return request.cookies.get(session_name)
