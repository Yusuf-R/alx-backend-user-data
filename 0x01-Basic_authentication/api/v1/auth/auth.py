#!/usr/bin/env python3
""" Base template for the auth functionality"""

from flask import request
from typing import List, TypeVar
from os import getenv
import re


# =============== require_auth ===============
# Returns True if path is None
# Returns True if excluded_paths is None or empty
# Returns False if path is in excluded_paths
# You can assume excluded_paths contains string path always ending by a /
# This method must be slash tolerant:
# path=/api/v1/status and path=/api/v1/status/
# must returned False if excluded_paths contains /api/v1/status/

class Auth():
    """ Base class for the auth
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        # sourcery skip: assign-if-exp, boolean-if-exp-identity, remove-unnecessary-cast, simplify-empty-collection-comparison, use-named-expression
        """ require_auth """
        if path is None or excluded_paths is None or excluded_paths == []:
            return True

        # synthezie path
        if path[-1] == '/':
            path = path[:-1]

        # Compile the regular expression pattern
        pattern = '|'.join(re.escape(p.rstrip('/')) for p in excluded_paths)

        # Compile the pattern into a regular expression object
        pattern = '({})'.format(pattern)

        match = re.search(pattern, path)

        # if the path matches the excluded paths, return False
        if match:
            return False
        else:
            return True

    def authorization_header(self, request=None) -> str:
        """ authorization_header """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ current_user """
        return None
